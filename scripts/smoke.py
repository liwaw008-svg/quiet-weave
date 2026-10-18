from pathlib import Path
import json, re, time
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

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
    {"label": "front desk", "detail": "Deliveries end by 10:00. The lobby is calm from 10:00 until the school group arrives at 13:00."},
    {"label": "room steward", "detail": "The ventilation hum is steady and low. Furniture reset runs from 12:30 to 13:15 near the east wall."},
    {"label": "programme calendar", "detail": "A reading circle occupies the room from 14:00. No amplified activity is scheduled before that session."},
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
(ROOT / "evidence" / "live-run.json").write_text(json.dumps(output, indent=2, default=str) + "\n", encoding="utf-8")
print(json.dumps(output, indent=2, default=str), flush=True)
