// Giao diện điện thoại cho quản lý nhân sự & phân công. JavaScript thuần, không thư viện.
// window.EMS_API (nếu có) thay cho API thật - dùng cho bản xem trước chạy không cần server.
(function () {
  "use strict";

  async function call(method, url, body) {
    const res = await fetch(url, {
      method,
      headers: body ? { "Content-Type": "application/json" } : {},
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await res.json().catch(() => ({}));
    if (res.status === 401 && url !== "/api/dang-nhap") showLogin();
    if (!res.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Lỗi máy chủ (" + res.status + ")");
    return data;
  }

  const api = window.EMS_API || {
    info: () => call("GET", "/api/info"),
    me: () => call("GET", "/api/toi"),
    login: (u, p) => call("POST", "/api/dang-nhap", { ten_dang_nhap: u, mat_khau: p }),
    logout: () => call("POST", "/api/dang-xuat"),
    list: () => call("GET", "/api/nhan-su"),
    phanCong: (id) => call("GET", "/api/nhan-su/" + id + "/phan-cong"),
    add: (id, noiDung) => call("POST", "/api/nhan-su/" + id + "/phan-cong", { noi_dung: noiDung }),
    ngung: (id) => call("POST", "/api/nhan-su/" + id + "/ngung"),
    kichHoat: (id) => call("POST", "/api/nhan-su/" + id + "/kich-hoat"),
  };

  const $ = (id) => document.getElementById(id);
  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  };

  let people = [];
  let me = null; // người đang đăng nhập: {ten_dang_nhap, ten, vai_tro}
  let filter = "all";
  let current = null; // nhân sự đang mở trong bảng trượt
  let lastFocus = null;

  // Mỗi trạm/tổ KCTX một màu cố định (theo tên đơn vị), giúp nhận ra nhanh trên danh sách.
  const PALETTE = ["#2563eb", "#7c3aed", "#db2777", "#ea580c", "#0891b2", "#16a34a", "#c026d3"];
  const unitColor = (p) => {
    let h = 0;
    for (const ch of p.DonVi || String(p.Id)) h = (h * 31 + ch.codePointAt(0)) >>> 0;
    return PALETTE[h % PALETTE.length];
  };
  const name = (p) => p.HoTen || "Nhân sự #" + p.Id;
  const meta = (p) => [p.DonVi, p.ChucDanh].filter(Boolean).join(" · ") || "Mã " + p.Id;
  const initials = (p) => name(p).split(/\s+/).slice(-2).map((w) => w[0]).join("").toUpperCase();
  const norm = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toLowerCase();

  function toast(msg, isErr) {
    const t = $("toast");
    t.textContent = msg;
    t.classList.toggle("err", !!isErr);
    t.hidden = false;
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => (t.hidden = true), 3200);
  }

  function statusChip(active) {
    return el("span", "status " + (active ? "on" : "off"), active ? "Đang làm" : "Đã ngừng");
  }

  function renderList() {
    const q = norm($("q").value.trim());
    const list = $("list");
    list.replaceChildren();
    const shown = people.filter((p) => {
      if (filter === "on" && !p.IsActive) return false;
      if (filter === "off" && p.IsActive) return false;
      return !q || norm(name(p) + " " + meta(p)).includes(q);
    });
    for (const p of shown) {
      const li = el("li");
      const b = el("button", "row " + (p.IsActive ? "on" : "off"));
      b.type = "button";
      b.style.setProperty("--c", unitColor(p));
      const text = el("div");
      text.append(el("div", "name", name(p)), el("div", "sub", meta(p)));
      b.append(el("span", "avatar", initials(p)), text, statusChip(p.IsActive));
      b.addEventListener("click", () => openSheet(p));
      li.append(b);
      list.append(li);
    }
    $("empty").hidden = shown.length > 0;
    const on = people.filter((p) => p.IsActive).length;
    $("counts").textContent = on + " đang làm · " + (people.length - on) + " đã ngừng";
  }

  async function load() {
    try {
      people = await api.list();
      renderList();
    } catch (e) {
      $("counts").textContent = "Không tải được";
      toast(e.message, true);
    }
  }

  function renderPhanCong(items) {
    const ul = $("s-pc");
    ul.replaceChildren();
    if (!items.length) ul.append(el("li", "none", "Chưa có phân công nào đang hiệu lực."));
    for (const it of items) ul.append(el("li", null, it.NoiDung));
  }

  function renderActions(p, pcCount) {
    const box = $("s-actions");
    box.replaceChildren();
    if (!me || me.vai_tro !== "quan_ly") {
      box.append(el("p", "hint", "Tài khoản của bạn chỉ có quyền xem."));
      return;
    }
    if (p.IsActive) {
      const b = el("button", "btn danger", "Ngừng nhân sự");
      b.type = "button";
      b.addEventListener("click", () => confirmNgung(p, pcCount));
      box.append(b);
    } else {
      const b = el("button", "btn", "Kích hoạt lại");
      b.type = "button";
      b.addEventListener("click", () => doKichHoat(p, b));
      box.append(b, el("p", "hint", "Phân công cũ không tự khôi phục; giao lại việc sau khi kích hoạt."));
    }
  }

  function confirmNgung(p, pcCount) {
    const box = $("s-actions");
    box.replaceChildren();
    const c = el("div", "confirm");
    c.append(el("p", null, "Ngừng " + name(p) + (pcCount ? " và " + pcCount + " phân công đang hiệu lực?" : "?")));
    const two = el("div", "two");
    const cancel = el("button", "btn", "Huỷ");
    cancel.type = "button";
    cancel.addEventListener("click", () => renderActions(p, pcCount));
    const ok = el("button", "btn danger solid", "Xác nhận ngừng");
    ok.type = "button";
    ok.addEventListener("click", () => doNgung(p, ok));
    two.append(cancel, ok);
    c.append(two);
    box.append(c);
    ok.focus();
  }

  async function doNgung(p, btn) {
    btn.disabled = true;
    try {
      const kq = await api.ngung(p.Id);
      toast("Đã ngừng " + name(p) + (kq.phan_cong_count ? " và " + kq.phan_cong_count + " phân công" : ""));
      await refreshCurrent(p.Id);
    } catch (e) {
      toast(e.message, true);
      btn.disabled = false;
    }
  }

  async function doKichHoat(p, btn) {
    btn.disabled = true;
    try {
      await api.kichHoat(p.Id);
      toast("Đã kích hoạt lại " + name(p));
      await refreshCurrent(p.Id);
    } catch (e) {
      toast(e.message, true);
      btn.disabled = false;
    }
  }

  async function refreshCurrent(id) {
    await load();
    const p = people.find((x) => x.Id === id);
    if (p) await fillSheet(p);
  }

  async function fillSheet(p) {
    current = p;
    $("sheet").style.setProperty("--c", unitColor(p));
    $("s-name").textContent = name(p);
    $("s-meta").textContent = meta(p);
    $("s-status").replaceWith(Object.assign(statusChip(p.IsActive), { id: "s-status" }));
    $("s-form").hidden = !p.IsActive || !me || me.vai_tro !== "quan_ly";
    $("s-pc").replaceChildren(el("li", "none", "Đang tải…"));
    let items = [];
    try {
      items = await api.phanCong(p.Id);
    } catch (e) {
      toast(e.message, true);
    }
    renderPhanCong(items);
    renderActions(p, items.length);
  }

  function openSheet(p) {
    lastFocus = document.activeElement;
    $("scrim").hidden = false;
    $("sheet").hidden = false;
    $("s-input").value = "";
    setHint();
    fillSheet(p);
    $("s-close").focus();
  }

  function closeSheet() {
    $("sheet").hidden = true;
    $("scrim").hidden = true;
    current = null;
    if (lastFocus) lastFocus.focus();
  }

  function setHint(msg) {
    const h = $("s-hint");
    h.textContent = msg || "Tối đa 500 ký tự.";
    h.classList.toggle("err", !!msg);
  }

  $("s-form").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const text = $("s-input").value.trim();
    if (!text) return setHint("Nhập nội dung phân công.");
    const btn = $("s-add");
    btn.disabled = true;
    try {
      const items = await api.add(current.Id, text);
      renderPhanCong(items);
      renderActions(current, items.length);
      $("s-input").value = "";
      setHint();
      toast("Đã giao việc cho " + name(current));
    } catch (e) {
      setHint(e.message);
    } finally {
      btn.disabled = false;
    }
  });

  $("s-close").addEventListener("click", closeSheet);
  $("scrim").addEventListener("click", closeSheet);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !$("sheet").hidden) closeSheet();
  });
  $("q").addEventListener("input", renderList);
  document.querySelectorAll(".chip").forEach((c) =>
    c.addEventListener("click", () => {
      filter = c.dataset.f;
      document.querySelectorAll(".chip").forEach((x) => x.setAttribute("aria-pressed", String(x === c)));
      renderList();
    })
  );

  // --- Đăng nhập ---------------------------------------------------------------
  function showLogin(msg) {
    me = null;
    people = [];
    if (!$("sheet").hidden) closeSheet();
    $("app").hidden = true;
    $("login").hidden = false;
    $("l-err").textContent = msg || "";
    $("l-pass").value = "";
    $("l-user").focus();
  }

  function startApp(user) {
    me = user;
    $("login").hidden = true;
    $("app").hidden = false;
    $("who-name").textContent = user.ten;
    $("who-role").textContent = user.vai_tro === "quan_ly" ? "Quản lý" : "Chỉ xem";
    load();
  }

  $("l-form").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const btn = $("l-btn");
    btn.disabled = true;
    $("l-err").textContent = "";
    try {
      startApp(await api.login($("l-user").value.trim(), $("l-pass").value));
    } catch (e) {
      $("l-err").textContent = e.message;
      $("l-pass").select();
    } finally {
      btn.disabled = false;
    }
  });

  $("logout").addEventListener("click", async () => {
    try {
      await api.logout();
    } catch (e) {
      /* phiên đã hết hạn thì coi như đã đăng xuất */
    }
    showLogin("Đã đăng xuất.");
  });

  api.info().then((i) => {
    $("demo").hidden = !i.demo;
    $("l-demo").hidden = !i.demo;
  }).catch(() => {});
  api.me().then(startApp).catch(() => showLogin());
})();
