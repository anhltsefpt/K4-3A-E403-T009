"""
evaluate.py — Chấm output AI so với golden set (số đo CP3, "bảng kết quả lượt 1 có %").

Tiêu chí "đúng" (đã chốt — phương án B, khắt khe):
  - bucket khớp, VÀ
  - do_now/soon: deadline khớp (so khớp chuẩn hoá, chứa nhau) VÀ kênh khớp
  - confirm: AI đặt needs_confirm = True
  - skip: AI trả bucket = skip

Chạy (sau khi đã gán nhãn golden mù + chạy classify.py):
    python src/classify.py golden/golden-set.csv > out/predictions.csv
    python src/evaluate.py golden/golden-set.csv out/predictions.csv
"""
import csv, sys, re


def norm(s):
    """Chuẩn hoá chuỗi deadline để so khớp mềm (bỏ dấu cách thừa, thường hoá)."""
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def _daynums(s):
    """Rút các số ngày/tháng/giờ/phút, BỎ năm (số ≥ 4 chữ số) — để so theo NGÀY,
    không phụ thuộc định dạng ('14/9' == '14/09/2026')."""
    return {int(x) for x in re.findall(r"\d+", s or "") if len(x) < 4}


def deadline_match(gt, pred):
    g, p = _daynums(gt), _daynums(pred)
    if not g:                       # golden không yêu cầu mốc cụ thể
        return True
    return g <= p or p <= g         # khớp theo tập số ngày/giờ (chứa nhau), bỏ định dạng


def judge(gt, pred):
    """Trả (đúng?, lý_do). gt/pred là dict."""
    b = gt["gt_bucket"].strip()
    if not b:
        return None, "golden CHƯA gán nhãn — bỏ qua dòng này"
    if pred is None:
        return False, "AI không trả kết quả cho tin này"
    pb = pred["bucket"].strip()
    if pb != b:
        return False, f"bucket sai: golden={b} · ai={pb}"
    if b in ("do_now", "soon"):
        if not deadline_match(gt["gt_deadline"], pred["deadline"]):
            return False, f"deadline sai: golden='{gt['gt_deadline']}' · ai='{pred['deadline']}'"
        if norm(gt["gt_source_channel"]) and norm(gt["gt_source_channel"]) != norm(pred["source_channel"]):
            return False, f"kênh sai: golden={gt['gt_source_channel']} · ai={pred['source_channel']}"
    if b == "confirm" and not str(pred["needs_confirm"]).lower().startswith("t"):
        return False, "cần needs_confirm=TRUE nhưng AI không đặt"
    return True, "OK"


def main():
    golden = {r["msg_id"]: r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8"))}
    preds = {r["msg_id"]: r for r in csv.DictReader(open(sys.argv[2], encoding="utf-8"))}

    n_ok = n_total = 0
    print(f"{'msg_id':10} {'golden':9} {'ai':9} {'kết quả'}")
    print("-" * 70)
    fails = []
    for mid, g in golden.items():
        ok, reason = judge(g, preds.get(mid))
        if ok is None:              # chưa gán nhãn
            continue
        n_total += 1
        n_ok += 1 if ok else 0
        pb = preds.get(mid, {}).get("bucket", "-")
        mark = "✅" if ok else "❌"
        print(f"{mid:10} {g['gt_bucket']:9} {pb:9} {mark} {reason}")
        if not ok:
            fails.append((mid, reason))

    print("-" * 70)
    pct = (100 * n_ok / n_total) if n_total else 0
    print(f"\nKẾT QUẢ LƯỢT 1: {n_ok}/{n_total} đúng = {pct:.0f}%")
    print(f"(chưa gán nhãn: {len(golden) - n_total} tin — hãy điền hết golden-set.csv)")
    if fails:
        print("\nCÁC CA SAI (dùng để phân tích 'vì sao sai' khi pitch — số xấu vẫn đủ điểm nếu trung thực):")
        for mid, r in fails:
            print(f"  • {mid}: {r}")


if __name__ == "__main__":
    main()
