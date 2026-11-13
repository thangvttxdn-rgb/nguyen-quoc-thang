// Kiểm thử giao diện trước/sau cho kỹ năng ctxdn-ui-ux-unslop (mô phỏng Chromium, KHÔNG phải thiết bị thật).
//
//   node kiem_tra_giao_dien.mjs <truoc.html> <sau.html> <thu-muc-ket-qua> [--kich-ban kich-ban.json]
//
// kich-ban.json: danh sách bước chạy trên cả hai bản, mỗi bước một trong:
//   {"dien": "#id", "gia_tri": "..."} · {"bam": "#id"} · {"cho": "#id"} · {"cho_an": "#id"} · {"chup": "ten-trang-thai"}
// Bấm (bam) không ép buộc: nếu phần tử bị che (vd. thông báo nổi đè lên nút), bước đó báo lỗi - đó là lỗi giao diện thật.
// Không có kịch bản thì chỉ chụp trạng thái lúc mở trang ("mo-trang").
// Kết quả: <thu-muc>/ket-qua.json và ảnh <ban>-<rong>-<trang-thai>.jpg. Mã thoát 0 = PASS, 1 = FAIL.

import { createRequire } from "node:module";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve, join } from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const RONG = [
  { rong: 360, cao: 740, ten: "Android nhỏ", dt: true },
  { rong: 390, cao: 844, ten: "iPhone", dt: true },
  { rong: 768, cao: 1024, ten: "Máy tính bảng", dt: true },
  { rong: 1366, cao: 768, ten: "Máy tính Windows", dt: false },
];
const CHU_TOI_THIEU = 12; // px
const NUT_TOI_THIEU = 44; // px, chiều cao vùng bấm trên màn hình cảm ứng

const args = process.argv.slice(2);
// Mã thoát: 0 = PASS, 1 = FAIL giao diện, 2 = lỗi công cụ/tham số (không phải kết luận về giao diện).
const loiCongCu = (msg) => { console.error("LỖI CÔNG CỤ: " + msg); process.exit(2); };
const viTri = args.indexOf("--kich-ban");
const [truoc, sau, raDir] = args.filter((a, i) => !a.startsWith("--") && (viTri < 0 || i !== viTri + 1));
if (!truoc || !sau || !raDir || (viTri >= 0 && !args[viTri + 1])) {
  loiCongCu("cách dùng: node kiem_tra_giao_dien.mjs <truoc.html> <sau.html> <thu-muc> [--kich-ban file.json]");
}
for (const f of [truoc, sau]) if (!existsSync(f)) loiCongCu(`không thấy file ${f}`);
let kichBan = [];
try { if (viTri >= 0) kichBan = JSON.parse(readFileSync(args[viTri + 1], "utf-8")); } catch (e) { loiCongCu(`đọc kịch bản: ${e.message}`); }
const BUOC = ["dien", "bam", "cho", "cho_an", "chup"];
const tenChup = new Set();
for (const b of kichBan) {
  const khoa = Object.keys(b).filter((k) => BUOC.includes(k));
  if (khoa.length !== 1) loiCongCu(`bước không hợp lệ: ${JSON.stringify(b)} (dùng một trong ${BUOC.join(", ")})`);
  if (b.chup) { if (tenChup.has(b.chup)) loiCongCu(`tên chụp trùng: ${b.chup}`); tenChup.add(b.chup); }
}
if (kichBan.length && !tenChup.size) loiCongCu("kịch bản không có bước chup nào - không đo được gì");
mkdirSync(raDir, { recursive: true });

// Bất biến nghiệp vụ đọc từ mã nguồn. Khung HTML = mã nguồn sau khi bỏ lớp trình bày (<style>,
// <link rel=stylesheet>, thuộc tính class/style, chú thích). Khung phải trùng khớp: mọi script (kể cả src),
// onclick, action/method, disabled/required, id/name… đều nằm trong khung.
const khungCua = (html) => html
  .replace(/<!--[\s\S]*?-->/g, "")
  .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, "")
  .replace(/<link\b[^>]*rel=["']?stylesheet["']?[^>]*>/gi, "")
  .replace(/\s(class|style)=("[^"]*"|'[^']*'|[^\s>]+)/gi, "")
  .replace(/\s+/g, " ").trim();
const scriptCua = (html) => [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]);
const dieuKhienCua = (html) =>
  [...html.matchAll(/<(button|a|input|select|textarea|form)\b([^>]*)>/gi)]
    .map((m) => {
      const thuocTinh = (ten) => {
        const k = m[2].match(new RegExp(`(?:^|\\s)${ten}=(?:"([^"]*)"|'([^']*)'|([^\\s>]+))`, "i"));
        return k ? k[1] ?? k[2] ?? k[3] : "";
      };
      return [m[1].toLowerCase(), thuocTinh("id"), thuocTinh("name"), thuocTinh("type"), thuocTinh("data-f"), thuocTinh("href")].join("|");
    })
    .sort();
const nguonTruoc = readFileSync(truoc, "utf-8");
const nguonSau = readFileSync(sau, "utf-8");
const sTruoc = scriptCua(nguonTruoc), sSau = scriptCua(nguonSau);
const dkTruoc = dieuKhienCua(nguonTruoc), dkSau = dieuKhienCua(nguonSau);
const kTruoc = khungCua(nguonTruoc), kSau = khungCua(nguonSau);
// Thiếu viewport thì trình duyệt điện thoại dựng trang khổ ~980px rồi thu nhỏ: số đo 360/390 vô nghĩa.
const coViewport = (html) => /<meta\b[^>]*name=["']?viewport["']?[^>]*width=device-width/i.test(html);
const batBien = {
  khung_html_trung_khop: kTruoc === kSau,
  viewport: [coViewport(nguonTruoc), coViewport(nguonSau)],
  script_trung_khop: sTruoc.length === sSau.length && sTruoc.every((s, i) => s === sSau[i]),
  so_script: [sTruoc.length, sSau.length],
  dieu_khien_trung_khop: JSON.stringify(dkTruoc) === JSON.stringify(dkSau),
  so_dieu_khien: [dkTruoc.length, dkSau.length],
  dieu_khien_mat: dkTruoc.filter((x) => !dkSau.includes(x)),
  dieu_khien_them: dkSau.filter((x) => !dkTruoc.includes(x)),
};

// Đo trong trang: tràn ngang, chữ nhỏ, nút nhỏ, nút bị che, chữ hiển thị.
function doTrang({ chuToiThieu, nutToiThieu, dienThoai }) {
  const hien = (e) => {
    const r = e.getBoundingClientRect();
    const cs = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && cs.visibility !== "hidden" && cs.display !== "none" && !e.closest("[hidden]");
  };
  const ten = (e) => e.tagName.toLowerCase() + (e.id ? "#" + e.id : "") + (e.className && typeof e.className === "string" ? "." + e.className.trim().split(/\s+/).join(".") : "");
  const chuNho = [];
  for (const e of document.querySelectorAll("body *")) {
    if (!hien(e) || e.closest(".sr")) continue;
    const coChu = [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    if (!coChu) continue;
    const co = parseFloat(getComputedStyle(e).fontSize);
    if (co < chuToiThieu) chuNho.push(`${ten(e)} ${co}px "${e.textContent.trim().slice(0, 30)}"`);
  }
  const nutNho = [], biChe = [];
  // Khi có hộp thoại modal đang mở, chỉ xét điều khiển bên trong nó (nền bị phủ là chủ ý).
  const modal = [...document.querySelectorAll('[aria-modal="true"]')].find(hien);
  // Lớp cố định hiển thị (trừ lớp phủ nền toàn màn hình và chính hộp modal).
  const phuCoDinh = [...document.querySelectorAll("body *")].filter((f) => {
    if (!hien(f) || f === modal || getComputedStyle(f).position !== "fixed") return false;
    const rf = f.getBoundingClientRect();
    return !(rf.width >= innerWidth - 1 && rf.height >= innerHeight - 1);
  });
  for (const e of (modal || document).querySelectorAll("button, a[href], input:not([type=hidden]), select, textarea")) {
    if (!hien(e)) continue;
    const r = e.getBoundingClientRect();
    if (dienThoai && r.height < nutToiThieu) nutNho.push(`${ten(e)} ${Math.round(r.width)}×${Math.round(r.height)}`);
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    // Nút đang cuộn khuất trong khung cuộn của nó: không phải bị che.
    let khuat = false;
    for (let a = e.parentElement; a; a = a.parentElement) {
      if (/(auto|scroll|hidden)/.test(getComputedStyle(a).overflowY)) {
        const ra = a.getBoundingClientRect();
        if (y < ra.top || y > ra.bottom || x < ra.left || x > ra.right) { khuat = true; break; }
      }
    }
    // Phần tử cố định (toast, thanh nổi) đè lên nút về mặt hiển thị - kể cả khi pointer-events: none.
    for (const f of phuCoDinh) {
      if (f.contains(e) || e.contains(f) || (modal && !modal.contains(f) && f.compareDocumentPosition(modal) & 4)) continue;
      const rf = f.getBoundingClientRect();
      if (!khuat && rf.left < r.right && rf.right > r.left && rf.top < r.bottom && rf.bottom > r.top) biChe.push(`${ten(e)} bị đè bởi ${ten(f)}`);
    }
    if (!khuat && x >= 0 && y >= 0 && x < innerWidth && y < innerHeight) {
      const tren = document.elementFromPoint(x, y);
      if (tren && tren !== e && !e.contains(tren) && !tren.contains(e) && !(e.labels && [...e.labels].some((l) => l.contains(tren)))) biChe.push(`${ten(e)} dưới ${ten(tren)}`);
    }
  }
  return {
    tran_ngang: document.documentElement.scrollWidth > innerWidth,
    rong_bo_cuc: innerWidth,
    rong_noi_dung: document.documentElement.scrollWidth,
    chu_nho: chuNho,
    nut_nho: nutNho,
    nut_bi_che: biChe,
    // Chữ trong DOM (không tính CSS text-transform): đổi nghĩa là đổi nội dung nghiệp vụ.
    chu_hien_thi: (() => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.parentElement.closest("script,style") ? 2 : 1) });
      let t = "";
      while (w.nextNode()) t += " " + w.currentNode.textContent;
      return t.replace(/\s+/g, " ").trim();
    })(),
  };
}

process.on("unhandledRejection", (e) => loiCongCu(String(e?.message || e).split("\n")[0]));
const trinhDuyet = await chromium.launch();
const phienBan = { playwright: require("playwright/package.json").version, chromium: trinhDuyet.version() };
const ketQua = { cong_cu: "Playwright + Chromium (mô phỏng)", phien_ban: phienBan, ngay: new Date().toISOString(), bat_bien: batBien, lan_chay: [] };

for (const [ban, file] of [["truoc", truoc], ["sau", sau]]) {
  for (const kc of RONG) {
    const trang = await trinhDuyet.newPage({ viewport: { width: kc.rong, height: kc.cao }, deviceScaleFactor: 1, isMobile: kc.dt && kc.rong < 768, hasTouch: kc.dt });
    const loiJs = [], loiMang = [];
    trang.on("pageerror", (e) => loiJs.push(String(e.message || e)));
    trang.on("console", (m) => { if (m.type() === "error") (/Failed to load resource|ERR_/.test(m.text()) ? loiMang : loiJs).push(m.text()); });
    trang.on("requestfailed", (r) => loiMang.push(r.url().slice(0, 80)));
    await trang.goto(pathToFileURL(resolve(file)).href, { waitUntil: "load" });
    await trang.waitForTimeout(400);
    const trangThai = [];
    const chup = async (tenTT) => {
      const anh = `${ban}-${kc.rong}-${tenTT}.jpg`;
      await trang.screenshot({ path: join(raDir, anh), type: "jpeg", quality: 70 });
      trangThai.push({ trang_thai: tenTT, anh, ...(await trang.evaluate(doTrang, { chuToiThieu: CHU_TOI_THIEU, nutToiThieu: NUT_TOI_THIEU, dienThoai: kc.dt })) });
    };
    if (!kichBan.length) await chup("mo-trang");
    for (const b of kichBan) {
      try {
        if (b.dien) await trang.fill(b.dien, b.gia_tri ?? "", { timeout: 3000 });
        else if (b.bam) await trang.click(b.bam, { timeout: 3000 });
        else if (b.cho) await trang.waitForSelector(b.cho, { state: "visible", timeout: 3000 });
        else if (b.cho_an) await trang.waitForSelector(b.cho_an, { state: "hidden", timeout: 8000 });
        else if (b.chup) await chup(b.chup);
        if (b.dien || b.bam) await trang.waitForTimeout(350);
      } catch (e) {
        trangThai.push({ trang_thai: "loi-kich-ban", buoc: b, loi: String(e.message).split("\n")[0] });
      }
    }
    ketQua.lan_chay.push({ ban, rong: kc.rong, thiet_bi: kc.ten, loi_js: loiJs, loi_mang: loiMang, trang_thai: trangThai });
    await trang.close();
  }
}
await trinhDuyet.close();

// Đánh giá: bản "sau" phải sạch; chữ hiển thị (nghiệp vụ) phải giống bản "truoc" ở mọi trạng thái.
const loi = [], ghiChu = [];
if (!batBien.viewport[1]) loi.push("Bản sau thiếu <meta name=viewport width=device-width> - số đo điện thoại không hợp lệ");
if (!batBien.khung_html_trung_khop) loi.push("Khung HTML (ngoài CSS/class/style) bị thay đổi");
if (!batBien.script_trung_khop) loi.push("Mã <script> bị thay đổi");
if (!batBien.dieu_khien_trung_khop) loi.push("Danh sách nút/ô nhập/biểu mẫu bị thay đổi");
for (const lc of ketQua.lan_chay.filter((l) => l.ban === "sau")) {
  const goc = ketQua.lan_chay.find((l) => l.ban === "truoc" && l.rong === lc.rong);
  if (lc.loi_js.length) loi.push(`${lc.rong}px: lỗi JavaScript ${lc.loi_js.length}`);
  const mangMoi = lc.loi_mang.filter((x) => !goc?.loi_mang.includes(x));
  if (mangMoi.length) loi.push(`${lc.rong}px: lỗi tải tài nguyên mới ${mangMoi.length}`);
  if (!lc.trang_thai.some((tt) => tt.trang_thai !== "loi-kich-ban")) loi.push(`${lc.rong}px: không đo được trạng thái nào`);
  for (const tt of lc.trang_thai) {
    const n = `${lc.rong}px/${tt.trang_thai}`;
    if (tt.trang_thai === "loi-kich-ban") { loi.push(`${n}: ${tt.loi}`); continue; }
    if (tt.tran_ngang) loi.push(`${n}: tràn ngang (${tt.rong_noi_dung}px)`);
    if (tt.rong_bo_cuc > lc.rong) loi.push(`${n}: bố cục dựng ở khổ ${tt.rong_bo_cuc}px, không phải ${lc.rong}px`);
    if (tt.chu_nho.length) loi.push(`${n}: chữ < ${CHU_TOI_THIEU}px ×${tt.chu_nho.length}`);
    if (tt.nut_nho.length) loi.push(`${n}: nút < ${NUT_TOI_THIEU}px ×${tt.nut_nho.length}`);
    if (tt.nut_bi_che.length) loi.push(`${n}: nút bị che ×${tt.nut_bi_che.length}`);
    // Chỉ so chữ khi bản trước đi tới trạng thái này mà chưa vấp lỗi kịch bản nào.
    const viTriGoc = goc ? goc.trang_thai.findIndex((x) => x.trang_thai === tt.trang_thai) : -1;
    const gocSach = viTriGoc >= 0 && !goc.trang_thai.slice(0, viTriGoc).some((x) => x.trang_thai === "loi-kich-ban");
    if (gocSach && goc.trang_thai[viTriGoc].chu_hien_thi !== tt.chu_hien_thi) loi.push(`${n}: chữ hiển thị khác bản trước`);
    if (!gocSach) ghiChu.push(`${n}: không so chữ được vì bản trước vấp lỗi kịch bản ở bước trước đó`);
  }
}
ketQua.ket_luan = loi.length ? "FAIL" : "PASS";
ketQua.loi = loi;
ketQua.ghi_chu = ghiChu;
// Lỗi của bản trước (để báo cáo, không tính vào kết luận).
ketQua.loi_ban_truoc = ketQua.lan_chay.filter((l) => l.ban === "truoc").flatMap((l) =>
  l.trang_thai.flatMap((tt) => tt.trang_thai === "loi-kich-ban" ? [`${l.rong}px: ${tt.loi}`] :
    [...(tt.tran_ngang ? [`${l.rong}px/${tt.trang_thai}: tràn ngang`] : []),
     ...tt.chu_nho.map((x) => `${l.rong}px/${tt.trang_thai}: chữ nhỏ ${x}`),
     ...tt.nut_nho.map((x) => `${l.rong}px/${tt.trang_thai}: nút nhỏ ${x}`),
     ...tt.nut_bi_che.map((x) => `${l.rong}px/${tt.trang_thai}: bị che ${x}`)]));
writeFileSync(join(raDir, "ket-qua.json"), JSON.stringify(ketQua, null, 2));
console.log(`${ketQua.ket_luan}: ${ketQua.lan_chay.length} lần chạy, ${loi.length} lỗi`);
for (const l of loi) console.log(" - " + l);
for (const g of ghiChu) console.log(" (ghi chú) " + g);
console.log(`Bản trước: ${ketQua.loi_ban_truoc.length} lỗi (chi tiết trong ket-qua.json)`);
process.exit(loi.length ? 1 : 0);
