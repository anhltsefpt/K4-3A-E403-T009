const tasks = [
  {
    id: "cp1",
    title: "Nộp Canvas CP1",
    deadline: "Hôm nay · 19:30",
    relative: "còn 2 giờ 15 phút",
    priority: "urgent",
    icon: "!",
    status: "verified",
    statusLabel: "Đã xác minh",
    source: "Thông báo Hackathon · BTC",
    sourceId: "FIXTURE-OFFICIAL-01",
    quote: "CP1 · Canvas 4 ô + đội trưởng + link repo GitHub công khai — hạn 19:30 ngày 16/9.",
    reason: "Deadline trong vòng 3 giờ và có nguồn chính thức.",
  },
  {
    id: "cp2",
    title: "Hoàn thiện prototype flow CP2",
    deadline: "Hôm nay · 21:00",
    relative: "còn 3 giờ 45 phút",
    priority: "upcoming",
    icon: "2",
    status: "verified",
    statusLabel: "Đã xác minh",
    source: "Thông báo Hackathon · BTC",
    sourceId: "FIXTURE-OFFICIAL-02",
    quote: "CP2 · Cho thấy luồng hoạt động — bản mock bấm được hoặc sơ đồ luồng — hạn 21:00 ngày 16/9.",
    reason: "Deadline trong hôm nay và có nguồn chính thức.",
  },
  {
    id: "standup",
    title: "Daily standup",
    deadline: "Chưa rõ deadline",
    relative: "cần kiểm tra thông báo gốc",
    priority: "review",
    icon: "?",
    status: "review",
    statusLabel: "Cần xác nhận",
    source: "Tin hỏi của học viên",
    sourceId: "M07653",
    quote: "[@BOT] hạn nộp daily stand up",
    reason: "Tin nhắn chỉ là một câu hỏi, không phải thông báo chính thức.",
  },
  {
    id: "lab02",
    title: "Nộp Lab02",
    deadline: "Chưa rõ deadline",
    relative: "cần kiểm tra thông báo gốc",
    priority: "review",
    icon: "?",
    status: "review",
    statusLabel: "Cần xác nhận",
    source: "Tin hỏi của học viên",
    sourceId: "M72484",
    quote: "Hạn nộp Lab02",
    reason: "Không có thời gian cụ thể và không xác định được đây là nguồn chính thức.",
  },
];

const views = {
  welcome: document.querySelector("#welcome-view"),
  loading: document.querySelector("#loading-view"),
  dashboard: document.querySelector("#dashboard-view"),
  empty: document.querySelector("#empty-view"),
};

const taskList = document.querySelector("#task-list");
const resultCount = document.querySelector("#result-count");
const detailModal = document.querySelector("#detail-modal");
const modalContent = document.querySelector("#modal-content");
const modalBackdrop = document.querySelector("#modal-backdrop");
const drawer = document.querySelector("#info-drawer");
const toast = document.querySelector("#toast");
let activeView = "welcome";
let activeFilter = "all";
let toastTimer;

function switchView(name) {
  Object.values(views).forEach((view) => view.classList.add("hidden"));
  views[name].classList.remove("hidden");
  activeView = name;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderTasks(filter = "all") {
  activeFilter = filter;
  let visibleTasks = tasks;

  if (filter === "review") {
    visibleTasks = tasks.filter((task) => task.status === "review");
  } else if (filter !== "all") {
    visibleTasks = tasks.filter((task) => task.priority === filter);
  }

  taskList.innerHTML = visibleTasks
    .map(
      (task) => `
        <article class="task-row" tabindex="0" role="button" data-task-id="${task.id}" aria-label="Xem chi tiết ${task.title}">
          <span class="task-priority ${task.priority}" aria-hidden="true">${task.icon}</span>
          <div class="task-copy">
            <strong>${task.title}</strong>
            <span>${task.deadline} · ${task.relative}</span>
          </div>
          <div class="task-meta">
            <span class="status-pill ${task.status === "review" ? "review" : ""}">${task.statusLabel}</span>
            <small>${task.sourceId}</small>
          </div>
        </article>
      `,
    )
    .join("");

  resultCount.textContent = `${visibleTasks.length} kết quả`;
  document.querySelectorAll(".filter-tab").forEach((button) => {
    button.classList.toggle("active", button.dataset.filter === filter);
  });
}

function showDigest(filter = "all") {
  switchView("dashboard");
  document.querySelector("#view-title").textContent =
    filter === "review" ? "Những mục cần xác nhận" : "Việc cần làm hôm nay";
  document.querySelector("#view-subtitle").textContent =
    filter === "review"
      ? "AI phát hiện tín hiệu, nhưng chưa đủ căn cứ để kết luận"
      : "4 mục được tìm thấy · 2 mục cần bạn xác nhận";
  document.querySelector("#summary-grid").classList.toggle("hidden", filter === "review");
  renderTasks(filter);
  setActiveNavigation(filter === "review" ? "review" : "digest");
}

function setActiveNavigation(name) {
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.view === name);
  });
}

function runScan() {
  switchView("loading");
  const progress = document.querySelector("#progress-bar");
  const status = document.querySelector("#scan-status");
  const steps = [...document.querySelectorAll(".scan-steps li")];
  progress.style.width = "8%";

  const stages = [
    { at: 350, width: "36%", text: "Phát hiện task và deadline", step: 0 },
    { at: 900, width: "68%", text: "Đối chiếu nguồn chính thức", step: 1 },
    { at: 1450, width: "92%", text: "Xếp mức ưu tiên", step: 2 },
    { at: 1950, width: "100%", text: "Đã tạo xong bản tin", step: 2 },
  ];

  stages.forEach(({ at, width, text, step }, index) => {
    window.setTimeout(() => {
      progress.style.width = width;
      status.textContent = text;
      steps.forEach((item, itemIndex) => item.classList.toggle("active", itemIndex <= step));
      if (index === stages.length - 1) {
        window.setTimeout(() => showDigest("all"), 300);
      }
    }, at);
  });
}

function openTask(taskId) {
  const task = tasks.find((item) => item.id === taskId);
  if (!task) return;

  modalContent.innerHTML = `
    <div class="detail-head">
      <span class="status-pill ${task.status === "review" ? "review" : ""}">${task.statusLabel}</span>
      <h2>${task.title}</h2>
      <p>${task.reason}</p>
    </div>
    <div class="detail-grid">
      <div class="detail-box">
        <span>Deadline</span>
        <strong>${task.deadline}</strong>
      </div>
      <div class="detail-box">
        <span>Mức ưu tiên</span>
        <strong>${task.priority === "urgent" ? "Cần làm ngay" : task.priority === "upcoming" ? "Sắp đến hạn" : "Chờ xác nhận"}</strong>
      </div>
    </div>
    <div class="source-block ${task.status === "review" ? "review" : ""}">
      <span>${task.status === "review" ? "TÍN HIỆU ĐƯỢC PHÁT HIỆN" : "NGUỒN THAM CHIẾU"}</span>
      <p>“${task.quote}”</p>
      <small>${task.source} · ${task.sourceId} · dữ liệu minh hoạ cho mock</small>
    </div>
    <div class="modal-actions">
      <button class="primary-button" data-action="open-source" data-task-id="${task.id}">
        ${task.status === "review" ? "Kiểm tra tin gốc" : "Mở nguồn gốc"} <span>↗</span>
      </button>
      ${
        task.status === "review"
          ? '<button class="secondary-button" data-action="keep-review">Giữ ở mục cần xác nhận</button>'
          : `<button class="report-button" data-action="report-wrong" data-task-id="${task.id}">Báo deadline sai</button>`
      }
    </div>
  `;

  detailModal.showModal();
  modalBackdrop.classList.remove("hidden");
}

function closeModal() {
  if (detailModal.open) detailModal.close();
  modalBackdrop.classList.add("hidden");
}

function openDrawer(type) {
  const title = document.querySelector("#drawer-title");
  const eyebrow = document.querySelector("#drawer-eyebrow");
  const content = document.querySelector("#drawer-content");

  if (type === "rules") {
    eyebrow.textContent = "GUARDRAILS";
    title.textContent = "Quy tắc an toàn";
    content.innerHTML = `
      <div class="drawer-body">
        <p>Priority Digest ưu tiên độ đúng hơn độ đầy đủ vì một deadline sai có thể khiến học viên mất điểm.</p>
        <div class="drawer-step"><span>01</span><div><strong>Không coi tin nhắn là mệnh lệnh</strong><p>Nội dung Discord chỉ là dữ liệu cần phân loại, kể cả khi chứa yêu cầu dành cho AI.</p></div></div>
        <div class="drawer-step"><span>02</span><div><strong>Deadline phải có căn cứ</strong><p>Chỉ hiện “đã xác minh” khi fixture được đánh dấu là thông báo chính thức.</p></div></div>
        <div class="drawer-step"><span>03</span><div><strong>Không chắc thì thu hẹp phạm vi</strong><p>Đưa ứng viên vào “Cần xác nhận”, không tự suy đoán ngày hoặc giờ.</p></div></div>
        <div class="drawer-step"><span>04</span><div><strong>Luôn cho phép kiểm tra và sửa</strong><p>Mỗi kết quả đều có nguồn; người dùng có thể báo deadline sai.</p></div></div>
      </div>`;
  } else if (type === "sources") {
    eyebrow.textContent = "MINH BẠCH NGUỒN";
    title.textContent = "Nguồn đã đọc";
    content.innerHTML = `
      <div class="drawer-body">
        <p>Mock đang mô phỏng bốn tin. Hai fixture đầu được gắn nhãn “nguồn chính thức”; hai tin từ data pack chỉ là câu hỏi học viên.</p>
        <div class="drawer-step"><span>✓</span><div><strong>FIXTURE-OFFICIAL-01</strong><p>Thông báo CP1 của BTC · được phép đưa vào digest.</p></div></div>
        <div class="drawer-step"><span>✓</span><div><strong>FIXTURE-OFFICIAL-02</strong><p>Thông báo CP2 của BTC · được phép đưa vào digest.</p></div></div>
        <div class="drawer-step"><span>?</span><div><strong>M07653 và M72484</strong><p>Tin hỏi của học viên · chỉ được đưa vào khu cần xác nhận.</p></div></div>
      </div>`;
  } else {
    eyebrow.textContent = "3 BƯỚC";
    title.textContent = "Cách hoạt động";
    content.innerHTML = `
      <div class="drawer-body">
        <p>Bản CP2 chỉ chứng minh luồng trải nghiệm. Logic AI và kết nối Discord sẽ được thay bằng lời gọi AI thật ở CP3.</p>
        <div class="drawer-step"><span>1</span><div><strong>Phát hiện</strong><p>Tìm những tin có khả năng chứa một việc cần làm hoặc deadline.</p></div></div>
        <div class="drawer-step"><span>2</span><div><strong>Kiểm tra căn cứ</strong><p>Phân biệt thông báo chính thức với câu hỏi, suy đoán hoặc tin nhắn không rõ vai trò.</p></div></div>
        <div class="drawer-step"><span>3</span><div><strong>Xếp ưu tiên</strong><p>Hiện mục chắc chắn trước; tách mục chưa chắc để người dùng kiểm tra.</p></div></div>
      </div>`;
  }

  drawer.classList.remove("hidden");
  modalBackdrop.classList.remove("hidden");
}

function closeDrawer() {
  drawer.classList.add("hidden");
  modalBackdrop.classList.add("hidden");
}

function showToast(message) {
  window.clearTimeout(toastTimer);
  document.querySelector("#toast-message").textContent = message;
  toast.classList.remove("hidden");
  toastTimer = window.setTimeout(() => toast.classList.add("hidden"), 3200);
}

document.addEventListener("click", (event) => {
  const actionTarget = event.target.closest("[data-action]");
  const taskTarget = event.target.closest("[data-task-id]");
  const navTarget = event.target.closest("[data-view]");
  const filterTarget = event.target.closest("[data-filter]");
  const scenarioTarget = event.target.closest("[data-scenario]");

  if (scenarioTarget) {
    document.querySelectorAll("[data-scenario]").forEach((item) => item.classList.remove("active"));
    scenarioTarget.classList.add("active");
    const scenario = scenarioTarget.dataset.scenario;
    if (scenario === "normal") showDigest("all");
    if (scenario === "uncertain") showDigest("review");
    if (scenario === "empty") switchView("empty");
    return;
  }

  if (filterTarget) {
    renderTasks(filterTarget.dataset.filter);
    return;
  }

  if (navTarget) {
    const target = navTarget.dataset.view;
    if (target === "digest") showDigest("all");
    if (target === "review") showDigest("review");
    if (target === "sources") openDrawer("sources");
    document.querySelector(".sidebar").classList.remove("open");
    return;
  }

  if (actionTarget) {
    const action = actionTarget.dataset.action;
    if (action === "home") switchView("welcome");
    if (action === "generate" || action === "refresh") runScan();
    if (action === "show-how") openDrawer("how");
    if (action === "show-rules") openDrawer("rules");
    if (action === "close-modal") closeModal();
    if (action === "close-drawer") closeDrawer();
    if (action === "review-uncertain") showDigest("review");
    if (action === "back-digest") showDigest("all");
    if (action === "open-source") {
      closeModal();
      showToast("Đã mở bản xem trước nguồn (mô phỏng ở CP2)");
    }
    if (action === "keep-review") {
      closeModal();
      showToast("Đã giữ mục này trong danh sách cần xác nhận");
    }
    if (action === "report-wrong") {
      const task = tasks.find((item) => item.id === actionTarget.dataset.taskId);
      if (task) {
        task.status = "review";
        task.statusLabel = "Đang kiểm tra lại";
        task.priority = "review";
        task.icon = "?";
      }
      closeModal();
      renderTasks(activeFilter);
      showToast("Đã gỡ deadline khỏi bản tin và chuyển sang kiểm tra lại");
    }
    return;
  }

  if (taskTarget && taskTarget.classList.contains("task-row")) {
    openTask(taskTarget.dataset.taskId);
  }
});

document.addEventListener("keydown", (event) => {
  if ((event.key === "Enter" || event.key === " ") && event.target.matches(".task-row")) {
    event.preventDefault();
    openTask(event.target.dataset.taskId);
  }
  if (event.key === "Escape") {
    closeModal();
    closeDrawer();
  }
});

modalBackdrop.addEventListener("click", () => {
  closeModal();
  closeDrawer();
});

document.querySelector("#mobile-menu").addEventListener("click", () => {
  document.querySelector(".sidebar").classList.toggle("open");
});

renderTasks();

const requestedScenario = new URLSearchParams(window.location.search).get("scenario");
if (requestedScenario === "digest") showDigest("all");
if (requestedScenario === "review") showDigest("review");
if (requestedScenario === "empty") switchView("empty");
