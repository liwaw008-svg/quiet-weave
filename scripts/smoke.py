from pathlib import Path
import json, re, time
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
import genlayer_py.contracts.actions as contract_actions

# StudioNet currently expects the legacy explicit `method` calldata key.
def compatible_calldata(method=None, args=None, kwargs=None):
    payload = {}
    if method is not None:
        payload["method"] = method
    if args:
        payload["args"] = args
    if kwargs:
        payload["kwargs"] = kwargs
    return payload

contract_actions.make_calldata_object = compatible_calldata

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text(encoding="utf-8")
KEY = re.search(r'^ACCOUNT_4_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()
client = create_client(chain=studionet, account=create_account(account_private_key=KEY))
deployment = json.loads((ROOT / "deployment.json").read_text(encoding="utf-8"))
address = deployment["contractAddress"]
loom_id = "LOOM-" + str(int(time.time()))
segments = [
    {"id": "B1", "start": 540, "end": 600, "label": "09:00"},
    {"id": "B2", "start": 600, "end": 660, "label": "10:00"},
    {"id": "B3", "start": 660, "end": 720, "label": "11:00"},
    {"id": "B4", "start": 720, "end": 780, "label": "12:00"},
    {"id": "B5", "start": 780, "end": 840, "label": "13:00"},
    {"id": "B6", "start": 840, "end": 900, "label": "14:00"},
]
observations = [
    {"label": "front desk log", "detail": "B1=LOUD because deliveries occupy the entrance. B2=QUIET because deliveries are complete and the room is undisturbed."},
    {"label": "room steward log", "detail": "B3=QUIET under the stated standard. B4=CONDITIONAL because readers must remain away from the east-wall furniture reset."},
    {"label": "programme calendar", "detail": "B5=LOUD because the school group and furniture reset overlap. B6=LOUD because a scheduled reading circle occupies the room."},
]
transactions = {}


def finalized(name, function, args):
    tx = client.write_contract(address=address, function_name=function, args=args)
    print(name + "_tx=" + str(tx), flush=True)
    receipt = client.wait_for_transaction_receipt(transaction_hash=tx, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
    leaders = receipt.get("consensus_data", {}).get("leader_receipt") or []
    leaders = [leaders] if isinstance(leaders, dict) else leaders
    assert receipt.get("result_name") == "MAJORITY_AGREE", receipt
    assert any(row.get("execution_result") == "SUCCESS" for row in leaders), receipt
    transactions[name] = str(tx)


finalized("set", "set_loom", [loom_id, "Shared reading room quiet window", "Africa/Casablanca", "Find at least two consecutive one-hour bands suitable for quiet reading, allowing only minor steady background sound.", json.dumps(segments), json.dumps(observations), 2])
finalized("weave", "weave_window", [loom_id])
record = client.read_contract(address=address, function_name="get_loom", args=[loom_id])
if record.get("outcome") == "WINDOW":
    finalized("pin", "pin_window", [loom_id])
    record = client.read_contract(address=address, function_name="get_loom", args=[loom_id])
output = {"recordType": "synthetic scheduling rehearsal; not a certified acoustic measurement", "loomId": loom_id, "contractAddress": address, "transactions": transactions, "readback": record}
(ROOT / "evidence").mkdir(exist_ok=True)
(ROOT / "evidence" / "live-run.json").write_text(json.dumps(output, indent=2, default=str) + "\n", encoding="utf-8")
print(json.dumps(output, indent=2, default=str), flush=True)
