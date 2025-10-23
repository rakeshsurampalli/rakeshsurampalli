const form = document.getElementById("contactForm");
const feedback = document.getElementById("formFeedback");
const yearSlot = document.getElementById("year");
// Ensure optional canvases are defined (null if absent in DOM)
const neuralCanvas = document.getElementById("neuralCanvas");
const stellarCanvas = document.getElementById("stellarCanvas");
const projectCards = document.querySelectorAll(".project-card");
const heroTooltip = document.getElementById("heroTooltip");
const heroTooltipTitle = document.getElementById("heroTooltipTitle");
const heroTooltipBody = document.getElementById("heroTooltipBody");
const heroSection = document.getElementById("hero");
const devToggle = document.getElementById("devToggle");
const devTerminal = document.getElementById("devTerminal");
const devTerminalOutput = document.getElementById("devTerminalOutput");
const devTerminalInput = document.getElementById("devTerminalInput");
const devTerminalDismiss = document.querySelectorAll("[data-terminal-dismiss]");
const magneticButtons = document.querySelectorAll(".btn--magnetic");
const revealTargets = document.querySelectorAll("[data-reveal]");
const heroBackground = heroSection ? heroSection.querySelector(".hero__background") : null;
const heroContent = heroSection ? heroSection.querySelector(".hero__content") : null;
const heroAside = heroSection ? heroSection.querySelector(".hero__aside") : null;
const introLoader = document.getElementById("introLoader");
const siteMain = document.querySelector(".site-main");
const introLoaderStatus = introLoader ? introLoader.querySelector(".intro-loader__status") : null;
const commandPalette = document.getElementById("commandPalette");
const commandPaletteInput = document.getElementById("commandPaletteInput");
const commandPaletteResults = document.getElementById("commandPaletteResults");
const commandPaletteDismiss = document.querySelectorAll("[data-command-dismiss]");
const commandPalettePanel = commandPalette ? commandPalette.querySelector(".command-palette__panel") : null;
const caseModal = document.getElementById("caseModal");
const caseModalTitle = document.getElementById("caseModalTitle");
const caseModalSummary = document.getElementById("caseModalSummary");
const caseModalReel = document.getElementById("caseModalReel");
const caseModalHighlights = document.getElementById("caseModalHighlights");
const caseModalImpact = document.getElementById("caseModalImpact");
const caseModalStack = document.getElementById("caseModalStack");
const caseModalConnect = document.getElementById("caseModalConnect");
const caseModalDismiss = document.querySelectorAll("[data-case-dismiss]");
const sceneSections = document.querySelectorAll("[data-scene]");
const timelineItems = document.querySelectorAll(".timeline__item");
const auroraCanvas = document.getElementById("auroraCanvas");

const clampValue = (value, min, max) => Math.min(Math.max(value, min), max);
const lerp = (start, end, t) => start + (end - start) * clampValue(t, 0, 1);
// Stellar, aurora, and neural canvas animation code removed

// No-op fallbacks for removed intro sequence helpers
// Prevent ReferenceError when initialization hooks are absent
const startIntroSequence = () => {};
const stopIntroSequence = () => {};

// Lightweight page scroll lock helpers (safe if called without CSS setup)
const lockBodyScroll = () => {
  try {
    document.documentElement.style.overflow = "hidden";
  } catch (_) {}
};
const unlockBodyScroll = () => {
  try {
    document.documentElement.style.overflow = "";
  } catch (_) {}
};

const hideIntroLoader = () => {
  if (introLoader && introLoader.classList.contains("is-hidden")) return;
  stopIntroSequence();
  if (siteMain) {
    siteMain.classList.add("is-ready");
  }
  if (introLoader) {
    introLoader.classList.add("is-hidden");
  }
};

if (introLoader) {
  startIntroSequence();
  // Primary: after all resources load
  window.addEventListener("load", () => {
    window.setTimeout(hideIntroLoader, 600);
  });
  // Fallback: after DOM is ready, in case some external assets block load
  document.addEventListener("DOMContentLoaded", () => {
    window.setTimeout(hideIntroLoader, 1200);
  });
  // Ultimate fallback: force-hide after a short delay even if above didn’t fire
  window.setTimeout(hideIntroLoader, 4000);
  window.addEventListener("keydown", (event) => {
    if (event.key === "Enter") hideIntroLoader();
  });
  introLoader.addEventListener("click", hideIntroLoader);
} else {
  hideIntroLoader();
}

let commandPaletteEntries = [];
let commandPaletteFiltered = [];
let commandPaletteSelection = 0;
let commandPaletteOpen = false;

const renderCommandPalette = (query = "") => {
  if (!commandPaletteResults) return;
  const normalized = query.trim().toLowerCase();
  commandPaletteFiltered = commandPaletteEntries.filter((entry) => {
    if (!normalized) return true;
    return entry.tokens.some((token) => token.includes(normalized));
  });
  commandPaletteSelection = commandPaletteFiltered.length ? 0 : -1;
  commandPaletteResults.innerHTML = "";
  commandPaletteFiltered.forEach((entry, index) => {
    const item = document.createElement("li");
    item.dataset.index = String(index);
    item.setAttribute("role", "option");
    if (index === commandPaletteSelection) item.setAttribute("aria-selected", "true");

    const label = document.createElement("span");
    label.textContent = entry.label;

    const shortcut = document.createElement("span");
    shortcut.className = "command-palette__shortcut";
    shortcut.textContent = entry.shortcut || "Enter";

    item.appendChild(label);
    item.appendChild(shortcut);
    commandPaletteResults.appendChild(item);
  });
};

const updateCommandPaletteSelection = (nextIndex) => {
  if (!commandPaletteResults || commandPaletteSelection === nextIndex) return;
  const items = commandPaletteResults.querySelectorAll("li");
  if (!items.length) return;
  commandPaletteSelection = ((nextIndex % items.length) + items.length) % items.length;
  items.forEach((node, idx) => {
    if (idx === commandPaletteSelection) {
      node.setAttribute("aria-selected", "true");
      node.scrollIntoView({ block: "nearest" });
    } else {
      node.removeAttribute("aria-selected");
    }
  });
};

const runCommandPaletteSelection = () => {
  if (!commandPaletteOpen || commandPaletteSelection < 0) {
    closeCommandPalette();
    return;
  }
  const entry = commandPaletteFiltered[commandPaletteSelection];
  if (!entry) return;
  const action = entry.action;
  if (commandPalette) {
    commandPalette.classList.add("is-executing");
  }
  window.setTimeout(() => {
    closeCommandPalette();
    window.setTimeout(() => {
      if (commandPalette) {
        commandPalette.classList.remove("is-executing");
      }
      action();
    }, 140);
  }, 180);
};

const getCommandPaletteFocusables = () => {
  if (!commandPalette) return [];
  return Array.from(
    commandPalette.querySelectorAll(
      "input, button, [role='option']"
    )
  );
};

const openCommandPalette = () => {
  if (!commandPalette || commandPaletteOpen) return;
  commandPaletteOpen = true;
  commandPalette.classList.add("is-open");
  commandPalette.classList.remove("is-executing");
  commandPalette.setAttribute("aria-hidden", "false");
  if (commandPalettePanel) {
    commandPalettePanel.style.animation = "none";
    // Force reflow to restart CSS animation sequence.
    void commandPalettePanel.offsetWidth;
    commandPalettePanel.style.animation = "";
  }
  renderCommandPalette("");
  if (commandPaletteInput) {
    commandPaletteInput.value = "";
    commandPaletteInput.focus();
  }
  lockBodyScroll();
};

const closeCommandPalette = () => {
  if (!commandPalette || !commandPaletteOpen) return;
  commandPaletteOpen = false;
  commandPalette.classList.remove("is-open");
  commandPalette.classList.remove("is-executing");
  commandPalette.setAttribute("aria-hidden", "true");
  commandPaletteSelection = -1;
  unlockBodyScroll();
};

const setCommandPaletteEntries = (entries) => {
  commandPaletteEntries = entries.map((entry) => ({
    ...entry,
    tokens: [entry.label, entry.description || "", ...(entry.keywords || [])].map((value) =>
      value.toLowerCase()
    ),
  }));
  renderCommandPalette(commandPaletteInput ? commandPaletteInput.value : "");
};

if (commandPalette) {
  Array.prototype.forEach.call(commandPaletteDismiss, (trigger) => {
    trigger.addEventListener("click", () => closeCommandPalette());
  });

  commandPalette.addEventListener("keydown", (event) => {
    if (!commandPaletteOpen) return;
    if (event.key === "Escape") {
      event.preventDefault();
      closeCommandPalette();
      return;
    }
    if (event.key === "Tab") {
      const focusable = getCommandPaletteFocusables();
      if (!focusable.length) return;
      const currentIndex = focusable.indexOf(document.activeElement);
      if (event.shiftKey) {
        event.preventDefault();
        const previous = (currentIndex - 1 + focusable.length) % focusable.length;
        focusable[previous].focus();
      } else {
        event.preventDefault();
        const next = (currentIndex + 1) % focusable.length;
        focusable[next].focus();
      }
    }
    if ((event.key === "ArrowDown" || event.key === "ArrowUp") && document.activeElement === commandPaletteInput) {
      event.preventDefault();
      const delta = event.key === "ArrowDown" ? 1 : -1;
      updateCommandPaletteSelection(commandPaletteSelection + delta);
    }
    if (event.key === "Enter" && document.activeElement === commandPaletteInput) {
      event.preventDefault();
      runCommandPaletteSelection();
    }
  });

  if (commandPaletteInput) {
    commandPaletteInput.addEventListener("input", (event) => {
      renderCommandPalette(event.target.value || "");
    });
  }

  if (commandPaletteResults) {
    commandPaletteResults.addEventListener("pointerdown", (event) => {
      const item = event.target.closest("li");
      if (!item) return;
      const rect = item.getBoundingClientRect();
      const x = clampValue((event.clientX - rect.left) / rect.width, 0, 1);
      const y = clampValue((event.clientY - rect.top) / rect.height, 0, 1);
      item.style.setProperty("--ink-x", `${(x * 100).toFixed(2)}%`);
      item.style.setProperty("--ink-y", `${(y * 100).toFixed(2)}%`);
      item.classList.add("is-inked");
      window.setTimeout(() => {
        item.classList.remove("is-inked");
      }, 260);
    });

    commandPaletteResults.addEventListener("mousemove", (event) => {
      const item = event.target.closest("li");
      if (!item) return;
      const index = Number.parseInt(item.dataset.index, 10);
      if (!Number.isNaN(index)) {
        updateCommandPaletteSelection(index);
      }
    });

    commandPaletteResults.addEventListener("click", (event) => {
      const item = event.target.closest("li");
      if (!item) return;
      const index = Number.parseInt(item.dataset.index, 10);
      if (Number.isNaN(index)) return;
      commandPaletteSelection = index;
      runCommandPaletteSelection();
    });
  }

  document.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key.toLowerCase() === "k") {
      event.preventDefault();
      if (commandPaletteOpen) {
        closeCommandPalette();
      } else {
        openCommandPalette();
      }
    }
  });
}

if (sceneSections.length && "IntersectionObserver" in window) {
  const sceneObserver = new IntersectionObserver(
    (entries) => {
      let dominant = null;
      entries.forEach((entry) => {
        entry.target.classList.toggle("is-active", entry.isIntersecting);
        if (!entry.isIntersecting) return;
        if (!dominant || entry.intersectionRatio > dominant.intersectionRatio) {
          dominant = entry;
        }
      });
      if (dominant) {
        const nextScene = dominant.target.dataset.scene;
        if (nextScene && nextScene !== activeScene) {
          activeScene = nextScene;
          document.body.dataset.scene = nextScene;
          document.dispatchEvent(new CustomEvent("scene-change", { detail: { scene: nextScene } }));
        }
      }
    },
    { threshold: 0.55, rootMargin: "0px 0px -15%" }
  );

  sceneSections.forEach((section) => {
    sceneObserver.observe(section);
  });
} else if (sceneSections.length) {
  sceneSections.forEach((section) => section.classList.add("is-active"));
}

if (timelineItems.length) {
  timelineItems.forEach((item, index) => {
    item.style.setProperty("--item-index", index);
  });
  if ("IntersectionObserver" in window) {
    const timelineObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-active");
          } else {
            entry.target.classList.remove("is-active");
          }
        });
      },
      { threshold: 0.6, rootMargin: "-10% 0px -10%" }
    );
    timelineItems.forEach((item) => timelineObserver.observe(item));
  } else {
    timelineItems.forEach((item) => item.classList.add("is-active"));
  }
}

const hydrateList = (target, items) => {
  if (!target) return;
  target.innerHTML = "";
  if (!items || !items.length) return;
  items.forEach((value, index) => {
    const entry = document.createElement("li");
    entry.textContent = value;
    entry.style.setProperty("--item-index", index);
    target.appendChild(entry);
  });
};

const hydrateReel = (items) => {
  if (!caseModalReel) return;
  caseModalReel.innerHTML = "";
  if (!items || !items.length) {
    caseModalReel.setAttribute("aria-hidden", "true");
    return;
  }
  items.forEach((item, index) => {
    const card = document.createElement("div");
    card.className = "case-modal__reel-item";
    card.style.setProperty("--item-index", index);
    const stat = document.createElement("strong");
    stat.textContent = item.stat;
    const label = document.createElement("span");
    label.textContent = item.label;
    card.appendChild(stat);
    card.appendChild(label);
    caseModalReel.appendChild(card);
  });
  caseModalReel.setAttribute("aria-hidden", "false");
};

const getCaseModalFocusables = () => {
  if (!caseModal) return [];
  return Array.from(
    caseModal.querySelectorAll("button, [href], input, textarea, select, [tabindex]:not([tabindex='-1'])")
  ).filter((node) => !node.hasAttribute("disabled") && node.getAttribute("aria-hidden") !== "true");
};

let caseModalActiveId = null;

const openCaseModal = (caseId) => {
  if (!caseModal || !caseStudies[caseId]) return false;
  const data = caseStudies[caseId];
  caseModalActiveId = caseId;
  caseModal.dataset.case = caseId;
  if (caseModalTitle) caseModalTitle.textContent = data.title;
  if (caseModalSummary) caseModalSummary.textContent = data.summary;
  hydrateReel(data.reel);
  hydrateList(caseModalHighlights, data.highlights);
  hydrateList(caseModalImpact, data.impact);
  hydrateList(caseModalStack, data.stack);
  caseModal.classList.add("is-open");
  caseModal.setAttribute("aria-hidden", "false");
  lockBodyScroll();
  requestAnimationFrame(() => {
    const focusables = getCaseModalFocusables();
    if (focusables.length) focusables[0].focus();
  });
  return true;
};

const closeCaseModal = () => {
  if (!caseModal || !caseModal.classList.contains("is-open")) return;
  caseModal.classList.remove("is-open");
  caseModal.setAttribute("aria-hidden", "true");
  caseModalActiveId = null;
  if (caseModalReel) {
    caseModalReel.setAttribute("aria-hidden", "true");
  }
  unlockBodyScroll();
};

const handleCaseModalKeydown = (event) => {
  if (!caseModal || !caseModal.classList.contains("is-open")) return;
  if (event.key === "Escape") {
    event.preventDefault();
    closeCaseModal();
    return;
  }
  if (event.key === "Tab") {
    const focusables = getCaseModalFocusables();
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }
};

document.addEventListener("keydown", handleCaseModalKeydown);

const scrollToSection = (id) => {
  const target = document.getElementById(id);
  if (target) {
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

const viewCaseStudy = (id) => {
  if (!openCaseModal(id)) {
    scrollToSection("projects");
  }
};

const buildCommandPaletteEntries = () => [
  {
    label: "Jump to Hero",
    description: "Scroll to the opening hero scene",
    keywords: ["home", "top", "intro"],
    shortcut: "Enter",
    action: () => scrollToSection("hero"),
  },
  {
    label: "Navigate to About",
    description: "Read the story behind the craft",
    keywords: ["about", "bio", "journey"],
    shortcut: "A",
    action: () => scrollToSection("about"),
  },
  {
    label: "Review Experience Timeline",
    description: "Highlight recent roles and wins",
    keywords: ["experience", "timeline", "roles"],
    shortcut: "E",
    action: () => scrollToSection("experience"),
  },
  {
    label: "Explore Projects",
    description: "Flip through featured builds",
    keywords: ["projects", "case", "work"],
    shortcut: "P",
    action: () => scrollToSection("projects"),
  },
  {
    label: "Contact Rakesh",
    description: "Scroll to the collaboration form",
    keywords: ["contact", "connect", "email"],
    shortcut: "C",
    action: () => scrollToSection("contact"),
  },
  {
    label: "Open Dev Mode Terminal",
    description: "Drop into the interactive console",
    keywords: ["terminal", "dev", "console"],
    shortcut: "Ctrl+`",
    action: () => toggleDevTerminal(true),
  },
  {
    label: "View Atlas Workspace Case Study",
    description: "Deep dive on knowledge orchestration",
    keywords: ["atlas", "workspace", "ai"],
    shortcut: "1",
    action: () => viewCaseStudy("atlas"),
  },
  {
    label: "View Pulse Insights Case Study",
    description: "Explore the customer health suite",
    keywords: ["pulse", "analytics", "insights"],
    shortcut: "2",
    action: () => viewCaseStudy("pulse"),
  },
  {
    label: "View Orbit Connect Case Study",
    description: "Inspect the integration fabric",
    keywords: ["orbit", "connect", "integration"],
    shortcut: "3",
    action: () => viewCaseStudy("orbit"),
  },
];

setCommandPaletteEntries(buildCommandPaletteEntries());

const currentYear = new Date().getFullYear();

if (yearSlot) {
  yearSlot.textContent = currentYear;
}

Array.prototype.forEach.call(caseModalDismiss, (element) => {
  element.addEventListener("click", () => closeCaseModal());
});

if (caseModal) {
  caseModal.addEventListener("click", (event) => {
    if (event.target === caseModal) {
      closeCaseModal();
    }
  });
}

if (caseModalConnect) {
  caseModalConnect.addEventListener("click", () => {
    closeCaseModal();
    scrollToSection("contact");
  });
}

const getAccentColor = () => getComputedStyle(document.body).getPropertyValue("--accent").trim() || "#38bdf8";

const hexToRgb = (value) => {
  const hex = value.startsWith("#") ? value.slice(1) : value;
  if (hex.length === 3) {
    const [r, g, b] = hex.split("");
    return {
      r: parseInt(r + r, 16),
      g: parseInt(g + g, 16),
      b: parseInt(b + b, 16),
    };
  }
  if (hex.length === 6) {
    return {
      r: parseInt(hex.slice(0, 2), 16),
      g: parseInt(hex.slice(2, 4), 16),
      b: parseInt(hex.slice(4, 6), 16),
    };
  }
  return null;
};

if (revealTargets.length) {
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2, rootMargin: "0px 0px -10%" }
    );

    revealTargets.forEach((element) => {
      const delay = parseFloat(element.dataset.revealDelay || "0");
      if (!Number.isNaN(delay)) {
        element.style.setProperty("--reveal-delay", `${delay}s`);
      }
      observer.observe(element);
    });
  } else {
    revealTargets.forEach((element) => {
      element.classList.add("is-visible");
    });
  }
}

if (magneticButtons.length) {
  const strength = 0.18;
  magneticButtons.forEach((button) => {
    button.addEventListener("pointermove", (event) => {
      if (event.pointerType && event.pointerType !== "mouse") return;
      const rect = button.getBoundingClientRect();
      const offsetX = event.clientX - rect.left - rect.width / 2;
      const offsetY = event.clientY - rect.top - rect.height / 2;
      button.style.setProperty("--magnet-x", `${offsetX * strength}px`);
      button.style.setProperty("--magnet-y", `${offsetY * strength}px`);
      button.classList.add("is-magnet-active");
      const now = performance.now();
      const last = magnetParticleCooldown.get(button) || 0;
      if (now - last > 70) {
        spawnMagnetParticle(button, offsetX, offsetY, 0.8);
        magnetParticleCooldown.set(button, now);
      }
    });

    button.addEventListener("pointerleave", () => {
      button.style.setProperty("--magnet-x", "0px");
      button.style.setProperty("--magnet-y", "0px");
      button.classList.remove("is-magnet-active");
      button.classList.remove("is-magnet-pressed");
      magnetParticleCooldown.delete(button);
    });

    button.addEventListener("pointerdown", (event) => {
      if (event.pointerType && event.pointerType !== "mouse") return;
      button.classList.add("is-magnet-pressed");
      const rect = button.getBoundingClientRect();
      const offsetX = event.clientX - rect.left - rect.width / 2;
      const offsetY = event.clientY - rect.top - rect.height / 2;
      for (let i = 0; i < 3; i += 1) {
        const angle = (Math.random() * Math.PI) / 3 - Math.PI / 6;
        const radius = 12 + Math.random() * 12;
        const dx = offsetX + Math.cos(angle) * radius;
        const dy = offsetY + Math.sin(angle) * radius;
        spawnMagnetParticle(button, dx, dy, 1.2);
      }
    });

    button.addEventListener("pointerup", () => {
      button.classList.remove("is-magnet-pressed");
    });

    button.addEventListener("blur", () => {
      button.style.setProperty("--magnet-x", "0px");
      button.style.setProperty("--magnet-y", "0px");
      button.classList.remove("is-magnet-active");
      button.classList.remove("is-magnet-pressed");
    });
  });
}

if (form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const name = formData.get("name");
    const email = formData.get("email");
    const message = formData.get("message");

    if (!name || !email || !message) {
      feedback.textContent = "Please complete all fields before sending.";
      feedback.style.color = "#f97316";
      return;
    }

    feedback.textContent = "Thanks for reaching out! I will respond soon.";
    feedback.style.color = "#38bdf8";
    form.classList.add("is-success");
    window.setTimeout(() => {
      form.classList.remove("is-success");
    }, 700);
    form.reset();
  });
}

if (stellarCanvas) {
  const ctx = stellarCanvas.getContext("2d");
  const config = {
    starDensity: 0.00018,
    minStars: 80,
    maxStars: 220,
    drift: 0.12,
    glow: 0.6,
    pointerRadius: 140,
  };
  let width = 0;
  let height = 0;
  let stars = [];
  const pulses = [];
  const pointer = { x: 0, y: 0, active: false };
  let pointerRadius = config.pointerRadius;

  const createStar = () => ({
    x: Math.random() * width,
    y: Math.random() * height,
    depth: 0.4 + Math.random() * 0.6,
    vx: (Math.random() - 0.5) * config.drift,
    vy: (Math.random() - 0.5) * config.drift,
  });

  const resize = () => {
    const rect = stellarCanvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    width = rect.width;
    height = rect.height;
    stellarCanvas.width = Math.round(width * dpr);
    stellarCanvas.height = Math.round(height * dpr);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
    const targetCount = Math.round(width * height * config.starDensity);
    const clamped = Math.max(config.minStars, Math.min(config.maxStars, targetCount));
    stars = Array.from({ length: clamped }, createStar);
    pointerRadius = Math.max(config.pointerRadius, Math.min(220, Math.sqrt(width + height) * 3.4));
  };

  const updatePointer = (event) => {
    const rect = stellarCanvas.getBoundingClientRect();
    pointer.x = event.clientX - rect.left;
    pointer.y = event.clientY - rect.top;
    pointer.active = pointer.x >= 0 && pointer.y >= 0 && pointer.x <= width && pointer.y <= height;
  };

  const draw = () => {
    ctx.clearRect(0, 0, width, height);
    const accent = getAccentColor();
    const accentRgb = hexToRgb(accent) || { r: 56, g: 189, b: 248 };

    const gradient = ctx.createLinearGradient(0, 0, width, height);
    gradient.addColorStop(0, "rgba(8, 47, 73, 0.85)");
    gradient.addColorStop(1, "rgba(15, 23, 42, 0.35)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);

    stars.forEach((star) => {
      star.x += star.vx * star.depth;
      star.y += star.vy * star.depth;

      if (star.x < -10) star.x = width + 10;
      if (star.x > width + 10) star.x = -10;
      if (star.y < -10) star.y = height + 10;
      if (star.y > height + 10) star.y = -10;

      const radius = 1.2 + star.depth * 1.5;
      const twinkle = (Math.sin(Date.now() * 0.002 + star.x) + 1) * 0.25;
      ctx.fillStyle = `rgba(${accentRgb.r}, ${accentRgb.g}, ${accentRgb.b}, ${0.2 + twinkle})`;
      ctx.beginPath();
      ctx.arc(star.x, star.y, radius, 0, Math.PI * 2);
      ctx.fill();

      if (pointer.active) {
        const dx = pointer.x - star.x;
        const dy = pointer.y - star.y;
        const distance = Math.hypot(dx, dy);
        if (distance < pointerRadius) {
          const strength = 1 - distance / pointerRadius;
          ctx.strokeStyle = `rgba(${accentRgb.r}, ${accentRgb.g}, ${accentRgb.b}, ${strength * config.glow})`;
          ctx.lineWidth = strength * 1.5;
          ctx.beginPath();
          ctx.moveTo(star.x, star.y);
          ctx.lineTo(pointer.x, pointer.y);
          ctx.stroke();
          star.x -= dx * 0.0006;
          star.y -= dy * 0.0006;
        }
      }
    });

    pulses.forEach((pulse, index) => {
      pulse.radius += 1.4;
      pulse.alpha -= 0.02;
      if (pulse.alpha <= 0) {
        pulses.splice(index, 1);
        return;
      }
      ctx.strokeStyle = `rgba(${accentRgb.r}, ${accentRgb.g}, ${accentRgb.b}, ${pulse.alpha})`;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.arc(pulse.x, pulse.y, pulse.radius, 0, Math.PI * 2);
      ctx.stroke();
    });

    requestAnimationFrame(draw);
  };

  resize();
  requestAnimationFrame(draw);

  if (heroSection) {
    heroSection.addEventListener("pointermove", updatePointer);
    heroSection.addEventListener("pointerleave", () => {
      pointer.active = false;
    });
    heroSection.addEventListener("click", (event) => {
      if (event.target.closest("a, button, input, textarea")) return;
      updatePointer(event);
      pulses.push({ x: pointer.x, y: pointer.y, radius: 6, alpha: 0.75 });
      stars.forEach((star) => {
        const dx = pointer.x - star.x;
        const dy = pointer.y - star.y;
        const distance = Math.hypot(dx, dy);
        if (distance < pointerRadius) {
          star.vx -= dx * 0.0005;
          star.vy -= dy * 0.0005;
        }
      });
    });
  }

  if (window.ResizeObserver) {
    new ResizeObserver(() => resize()).observe(stellarCanvas);
  } else {
    window.addEventListener("resize", resize);
  }
}

if (auroraCanvas) {
  const ctx = auroraCanvas.getContext("2d");
  const waves = [
    { amplitude: 42, wavelength: 260, speed: 0.00022, phase: 0 },
    { amplitude: 28, wavelength: 180, speed: 0.00034, phase: Math.PI / 2 },
  ];
  let width = 0;
  let height = 0;
  let colors = null;
  const pointer = { x: 0.5, y: 0.35, targetX: 0.5, targetY: 0.35 };

  const readColors = () => {
    const computed = getComputedStyle(document.body);
    return {
      primary: computed.getPropertyValue("--aurora-primary").trim() || "rgba(56, 189, 248, 0.2)",
      secondary: computed.getPropertyValue("--aurora-secondary").trim() || "rgba(14, 165, 233, 0.14)",
    };
  };

  const resize = () => {
    const rect = auroraCanvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    width = rect.width;
    height = rect.height;
    auroraCanvas.width = Math.round(rect.width * dpr);
    auroraCanvas.height = Math.round(rect.height * dpr);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
  };

  const updatePointer = (event) => {
    if (!heroSection) return;
    const rect = heroSection.getBoundingClientRect();
    const relativeX = clampValue((event.clientX - rect.left) / rect.width, 0, 1);
    const relativeY = clampValue((event.clientY - rect.top) / rect.height, 0, 1);
    pointer.targetX = relativeX;
    pointer.targetY = relativeY * 0.8;
  };

  const draw = (timestamp = 0) => {
    if (!width || !height) {
      requestAnimationFrame(draw);
      return;
    }
    pointer.x = lerp(pointer.x, pointer.targetX, 0.06);
    pointer.y = lerp(pointer.y, pointer.targetY, 0.06);
    ctx.clearRect(0, 0, width, height);
    ctx.globalCompositeOperation = "lighter";

    waves.forEach((wave, index) => {
      ctx.beginPath();
      ctx.moveTo(0, height);
      const base = height * (0.45 + index * 0.12);
      const step = Math.max(8, width / 160);
      for (let x = 0; x <= width + step; x += step) {
        const angle = timestamp * wave.speed + (x / wave.wavelength) + wave.phase;
        const offset = Math.sin(angle) * wave.amplitude;
        const pointerInfluence = Math.cos((x / width - pointer.x) * Math.PI) * pointer.y * 40;
        const y = base + offset - pointerInfluence;
        ctx.lineTo(x, y);
      }
      ctx.lineTo(width, height);
      ctx.closePath();
      if (!colors) colors = readColors();
      const gradient = ctx.createLinearGradient(0, 0, width, height);
      const tint = index === 0 ? colors.primary : colors.secondary;
      gradient.addColorStop(0, tint);
      gradient.addColorStop(1, "rgba(15, 23, 42, 0)");
      ctx.fillStyle = gradient;
      ctx.fill();
    });

    ctx.globalCompositeOperation = "source-over";
    requestAnimationFrame(draw);
  };

  colors = readColors();
  resize();
  requestAnimationFrame(draw);

  if (heroSection) {
    heroSection.addEventListener("pointermove", updatePointer);
    heroSection.addEventListener("pointerleave", () => {
      pointer.targetX = 0.5;
      pointer.targetY = 0.35;
    });
  }

  if (window.ResizeObserver) {
    new ResizeObserver(() => resize()).observe(auroraCanvas);
  } else {
    window.addEventListener("resize", resize);
  }

  document.addEventListener("time-theme-change", () => {
    colors = readColors();
  });
}

if (projectCards.length) {
  const peekTimers = new WeakMap();

  const clearPeekTimers = (card) => {
    const timers = peekTimers.get(card);
    if (timers) {
      timers.forEach((id) => window.clearTimeout(id));
      peekTimers.delete(card);
    }
  };

  const schedulePeek = (card) => {
    if (!card || card.classList.contains("is-flipped")) return;
    clearPeekTimers(card);
    const timers = [];
    const startId = window.setTimeout(() => {
      if (card.classList.contains("is-hovered") || card.matches(":hover")) {
        clearPeekTimers(card);
        return;
      }
      card.classList.add("is-peeking");
      const endId = window.setTimeout(() => {
        card.classList.remove("is-peeking");
        clearPeekTimers(card);
      }, 1400);
      timers.push(endId);
      peekTimers.set(card, timers);
    }, 280);
    timers.push(startId);
    peekTimers.set(card, timers);
  };

  if ("IntersectionObserver" in window) {
    const peekObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const card = entry.target;
          if (entry.isIntersecting) {
            schedulePeek(card);
          } else {
            clearPeekTimers(card);
            card.classList.remove("is-peeking");
          }
        });
      },
      { threshold: 0.55 }
    );

    projectCards.forEach((card) => {
      peekObserver.observe(card);
    });
  } else {
    projectCards.forEach((card) => {
      schedulePeek(card);
    });
  }

  const getTilt = (card, event) => {
    const rect = card.getBoundingClientRect();
    const relativeX = (event.clientX - rect.left) / rect.width;
    const relativeY = (event.clientY - rect.top) / rect.height;
    const rotateY = (relativeX - 0.5) * 18;
    const rotateX = (0.5 - relativeY) * 14;
    card.style.transform = `rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg)`;
  };

  const resetTilt = (card) => {
    card.style.transform = "";
  };

  projectCards.forEach((card) => {
    const frontFace = card.querySelector(".project-card__face--front");
    const backFace = card.querySelector(".project-card__face--back");
    if (frontFace) frontFace.setAttribute("aria-hidden", "false");
    if (backFace) backFace.setAttribute("aria-hidden", "true");
    const toggle = () => {
      const flipped = card.classList.toggle("is-flipped");
      card.setAttribute("aria-expanded", String(flipped));
      if (frontFace) frontFace.setAttribute("aria-hidden", flipped ? "true" : "false");
      if (backFace) backFace.setAttribute("aria-hidden", flipped ? "false" : "true");
      if (flipped) {
        clearPeekTimers(card);
        card.classList.remove("is-peeking");
      }
    };

    card.addEventListener("pointerenter", (event) => {
      if (event.pointerType && event.pointerType !== "mouse") return;
      clearPeekTimers(card);
      card.classList.remove("is-peeking");
      card.classList.add("is-hovered");
    });

    card.addEventListener("pointermove", (event) => {
      if (event.pointerType !== "mouse") return;
      getTilt(card, event);
    });

    card.addEventListener("pointerleave", () => {
      resetTilt(card);
      card.classList.remove("is-hovered");
    });

    card.addEventListener("click", (event) => {
      if (event.target.closest(".project-card__link")) return;
      clearPeekTimers(card);
      card.classList.remove("is-peeking");
      toggle();
    });

    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        clearPeekTimers(card);
        card.classList.remove("is-peeking");
        toggle();
      }
    });
  });

  const projectLinks = document.querySelectorAll(".project-card__link");
  projectLinks.forEach((element) => {
    element.addEventListener("click", (event) => {
      event.stopPropagation();
      const caseId = element.dataset.case;
      if (caseId) {
        viewCaseStudy(caseId);
        return;
      }
      const scrollTarget = element.dataset.scroll;
      if (scrollTarget) {
        scrollToSection(scrollTarget);
      }
    });
  });
}

if (neuralCanvas) {
  // Interactive node explorer for the hero canvas.
  const ctx = neuralCanvas.getContext("2d");
  const config = {
    nodeDensity: 0.00008,
    minNodes: 28,
    maxNodes: 72,
    maxDistance: 150,
    velocity: 0.22,
    hoverRadius: 110,
  };
  const pointer = { x: 0, y: 0, active: false };
  const payloads = [
    {
      title: "AI Ops Automations",
      body: "Self-healing playbooks triage incidents and trigger observability pipelines without human bottlenecks.",
    },
    {
      title: "Inclusive Dashboards",
      body: "WCAG-compliant visuals and narration-ready data stories improve signal clarity for every stakeholder.",
    },
    {
      title: "Edge Deployments",
      body: "Zero-downtime rollouts across multi-cloud edges keep latency-sensitive workloads resilient.",
    },
    {
      title: "Data Mesh Tooling",
      body: "Domain-aligned contracts align producer and consumer teams with frictionless governance gates.",
    },
    {
      title: "Mentorship Circuits",
      body: "Structured guidance programs pair emerging engineers with growth tracks rooted in real delivery work.",
    },
  ];

  let viewWidth = 0;
  let viewHeight = 0;
  let nodes = [];
  let activeNodeIndex = null;
  let nodeCount = config.minNodes;
  let maxDistance = config.maxDistance;
  let hoverRadius = config.hoverRadius;
  const pointerTarget = heroSection || neuralCanvas;

  const createNode = () => ({
    x: Math.random() * viewWidth,
    y: Math.random() * viewHeight,
    vx: (Math.random() - 0.5) * config.velocity,
    vy: (Math.random() - 0.5) * config.velocity,
    phase: Math.random() * Math.PI * 2,
  });

  const assignPayloads = () => {
    nodes.forEach((node) => {
      delete node.payload;
    });
    const available = nodes.slice();
    payloads.forEach((payload) => {
      if (!available.length) return;
      const index = Math.floor(Math.random() * available.length);
      const node = available.splice(index, 1)[0];
      node.payload = payload;
    });
  };

  const calculateNodeCount = () => {
    const target = Math.round(viewWidth * viewHeight * config.nodeDensity);
    return Math.max(config.minNodes, Math.min(config.maxNodes, target));
  };

  const populateNodes = () => {
    nodeCount = calculateNodeCount();
    nodes = Array.from({ length: nodeCount }, createNode);
    assignPayloads();
  };

  const resize = () => {
    const rect = heroSection ? heroSection.getBoundingClientRect() : neuralCanvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    viewWidth = rect.width;
    viewHeight = rect.height;
    neuralCanvas.width = Math.round(rect.width * dpr);
    neuralCanvas.height = Math.round(rect.height * dpr);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
    maxDistance = Math.min(220, Math.max(140, Math.sqrt((viewWidth + viewHeight) / 2) * 2.8));
    hoverRadius = Math.min(150, Math.max(95, maxDistance * 0.7));
    populateNodes();
    activeNodeIndex = null;
    hideTooltip();
  };

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

  const positionTooltip = (x, y) => {
    if (!heroTooltip) return;
    const tooltipRect = heroTooltip.getBoundingClientRect();
    const width = tooltipRect.width || 220;
    const height = tooltipRect.height || 120;
    const px = clamp(x - width / 2, 16, viewWidth - width - 16);
    const py = clamp(y - height - 20, 16, viewHeight - height - 16);
    heroTooltip.style.transform = `translate3d(${px}px, ${py}px, 0)`;
  };

  const showTooltip = (node) => {
    if (!heroTooltip || !heroTooltipTitle || !heroTooltipBody || !node || !node.payload) return;
    heroTooltipTitle.textContent = node.payload.title;
    heroTooltipBody.textContent = node.payload.body;
    heroTooltip.hidden = false;
    requestAnimationFrame(() => {
      positionTooltip(node.x, node.y);
      heroTooltip.classList.add("is-active");
    });
  };

  function hideTooltip() {
    if (!heroTooltip) return;
    heroTooltip.classList.remove("is-active");
    heroTooltip.hidden = true;
  }

  const setActiveNode = () => {
    if (!pointer.active) {
      activeNodeIndex = null;
      hideTooltip();
      return;
    }
    let nearestIndex = null;
    let nearestDistance = hoverRadius;
    nodes.forEach((node, index) => {
      const distance = Math.hypot(pointer.x - node.x, pointer.y - node.y);
      if (distance < nearestDistance) {
        nearestDistance = distance;
        nearestIndex = index;
      }
    });
    if (nearestIndex !== activeNodeIndex) hideTooltip();
    activeNodeIndex = nearestIndex;
  };

  const updatePointer = (event) => {
    const rect = heroSection ? heroSection.getBoundingClientRect() : neuralCanvas.getBoundingClientRect();
    pointer.x = event.clientX - rect.left;
    pointer.y = event.clientY - rect.top;
    pointer.active = pointer.x >= 0 && pointer.y >= 0 && pointer.x <= viewWidth && pointer.y <= viewHeight;
    setActiveNode();
  };

  const draw = () => {
    ctx.clearRect(0, 0, viewWidth, viewHeight);
    const accent = getAccentColor();
    const accentRgb = hexToRgb(accent) || { r: 56, g: 189, b: 248 };

    nodes.forEach((node, index) => {
      node.x += node.vx;
      node.y += node.vy;
      node.phase += 0.02;

      if (node.x <= 0 || node.x >= viewWidth) {
        node.vx *= -1;
        node.x = clamp(node.x, 0, viewWidth);
      }
      if (node.y <= 0 || node.y >= viewHeight) {
        node.vy *= -1;
        node.y = clamp(node.y, 0, viewHeight);
      }

      for (let j = index + 1; j < nodes.length; j += 1) {
        const other = nodes[j];
        const dx = node.x - other.x;
        const dy = node.y - other.y;
        const dist = Math.hypot(dx, dy);
        if (dist < maxDistance) {
          const intensity = 1 - dist / maxDistance;
          const activeBoost = index === activeNodeIndex || j === activeNodeIndex ? 0.5 : 0;
          ctx.strokeStyle = `rgba(${accentRgb.r}, ${accentRgb.g}, ${accentRgb.b}, ${(intensity * 0.55) + activeBoost * 0.45})`;
          ctx.lineWidth = 1 + activeBoost;
          ctx.beginPath();
          ctx.moveTo(node.x, node.y);
          ctx.lineTo(other.x, other.y);
          ctx.stroke();
        }
      }

      const isActive = index === activeNodeIndex;
      const baseRadius = 2 + Math.sin(node.phase) * 0.4;
      const radius = isActive ? baseRadius + 2.6 : node.payload ? baseRadius + 1 : baseRadius;
      const alpha = isActive ? 1 : node.payload ? 0.85 : 0.65;
      ctx.fillStyle = `rgba(${accentRgb.r}, ${accentRgb.g}, ${accentRgb.b}, ${alpha})`;
      ctx.beginPath();
      ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
      ctx.fill();
    });

    if (pointer.active && activeNodeIndex !== null) {
      const node = nodes[activeNodeIndex];
      ctx.strokeStyle = `rgba(${accentRgb.r}, ${accentRgb.g}, ${accentRgb.b}, 0.6)`;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(node.x, node.y);
      ctx.lineTo(pointer.x, pointer.y);
      ctx.stroke();
    }

    requestAnimationFrame(draw);
  };

  resize();
  requestAnimationFrame(draw);

  if (pointerTarget) {
    pointerTarget.addEventListener("pointermove", updatePointer);
    pointerTarget.addEventListener("pointerleave", () => {
      pointer.active = false;
      activeNodeIndex = null;
      hideTooltip();
    });
    pointerTarget.addEventListener("click", (event) => {
      if (event.target.closest("a, button, input, textarea")) return;
      updatePointer(event);
      if (activeNodeIndex !== null) {
        const node = nodes[activeNodeIndex];
        if (node.payload) {
          showTooltip(node);
        }
        nodes.forEach((member) => {
          const dx = node.x - member.x;
          const dy = node.y - member.y;
          const dist = Math.hypot(dx, dy);
          if (dist < maxDistance) {
            member.vx -= dx * 0.0008;
            member.vy -= dy * 0.0008;
          }
        });
      }
    });
  }

  neuralCanvas.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      if (activeNodeIndex !== null) {
        showTooltip(nodes[activeNodeIndex]);
      }
    }
  });

  if (window.ResizeObserver) {
    new ResizeObserver(() => resize()).observe(heroSection || neuralCanvas);
  } else {
    window.addEventListener("resize", resize);
  }
}

const appendDevTerminalLine = (type, content) => {
  if (!devTerminalOutput) return;
  const line = document.createElement("div");
  line.className = "dev-terminal__line";

  const prompt = document.createElement("span");
  prompt.className = "dev-terminal__line__prompt";
  prompt.textContent = type === "input" ? "➜" : type === "error" ? "✖" : "★";

  const message = document.createElement("div");
  message.className = "dev-terminal__line__content";
  message.textContent = content;

  line.appendChild(prompt);
  line.appendChild(message);
  line.classList.add("is-new");
  line.addEventListener(
    "animationend",
    () => {
      line.classList.remove("is-new");
    },
    { once: true }
  );
  devTerminalOutput.appendChild(line);
  devTerminalOutput.scrollTop = devTerminalOutput.scrollHeight;
};

let devDemoKickoffTimer = null;
let devDemoTypingTimer = null;

const cancelDevTerminalDemo = () => {
  if (devDemoKickoffTimer !== null) {
    window.clearTimeout(devDemoKickoffTimer);
    devDemoKickoffTimer = null;
  }
  if (devDemoTypingTimer !== null) {
    window.clearTimeout(devDemoTypingTimer);
    devDemoTypingTimer = null;
  }
};

const startDevTerminalDemo = () => {
  if (!devTerminal || !devTerminalInput) return;
  cancelDevTerminalDemo();
  const demoCommand = "help";
  devTerminalInput.value = "";
  devDemoKickoffTimer = window.setTimeout(() => {
    let index = 0;
    const step = () => {
      if (!devTerminal.classList.contains("is-open")) {
        cancelDevTerminalDemo();
        return;
      }
      if (index <= demoCommand.length) {
        devTerminalInput.value = demoCommand.slice(0, index);
        index += 1;
        devDemoTypingTimer = window.setTimeout(step, 90);
        return;
      }
      appendDevTerminalLine("input", demoCommand);
      handleDevCommand(demoCommand);
      devTerminalInput.value = "";
      cancelDevTerminalDemo();
    };
    step();
  }, 700);
};

const bootDevTerminal = () => {
  if (!devTerminalOutput) return;
  devTerminalOutput.innerHTML = "";
  appendDevTerminalLine("system", "Initializing developer console...");
  appendDevTerminalLine(
    "system",
    'Type "help" to explore commands. Use Esc or type "exit" to close.'
  );
};

const toggleDevTerminal = (shouldOpen) => {
  if (!devTerminal) return;
  const open = typeof shouldOpen === "boolean" ? shouldOpen : !devTerminal.classList.contains("is-open");
  if (open) {
    devTerminal.classList.add("is-open");
  } else {
    devTerminal.classList.remove("is-open");
  }
  devTerminal.setAttribute("aria-hidden", open ? "false" : "true");

  if (open) {
    bootDevTerminal();
    startDevTerminalDemo();
    document.body.style.overflow = "hidden";
    requestAnimationFrame(() => {
      if (devTerminalInput) devTerminalInput.focus();
    });
  } else {
    cancelDevTerminalDemo();
    document.body.style.overflow = "";
    if (devToggle) devToggle.focus();
  }
  if (devToggle) devToggle.setAttribute("aria-expanded", open ? "true" : "false");
};

const getDevTerminalFocusables = () => {
  if (!devTerminal) return [];
  return Array.from(
    devTerminal.querySelectorAll(
      "button, [href], input, textarea, select, [tabindex]:not([tabindex='-1'])"
    )
  ).filter((node) => !node.hasAttribute("disabled") && node.getAttribute("aria-hidden") !== "true");
};

const handleDevCommand = (value) => {
  const command = value.trim();
  if (!command) {
    appendDevTerminalLine("system", "Awaiting your command...");
    return;
  }

  const normalized = command.toLowerCase();

  switch (normalized) {
    case "help":
      appendDevTerminalLine(
        "system",
        "Available commands: help, about, skills, experience, projects, contact, theme, exit."
      );
      break;
    case "about":
      appendDevTerminalLine(
        "system",
        "Rakesh Surampalli — crafting secure, resilient systems; blending backend expertise with immersive front-end experiences."
      );
      break;
    case "skills":
      appendDevTerminalLine(
        "system",
        "Core stack: TypeScript, Node.js, React, AWS. Toolbelt: GraphQL, Docker, Terraform, Next.js, Figma."
      );
      break;
    case "experience":
      appendDevTerminalLine(
        "system",
        "Latest: Senior Software Engineer @ TechNova. Previously: InnovateX, CloudScale. Delivering end-to-end platform evolution."
      );
      break;
    case "projects":
      appendDevTerminalLine(
        "system",
        "Highlights: AetherOps automation suite, LatticeAI observability toolkit, PulseMesh real-time collaboration engine."
      );
      break;
    case "contact":
      appendDevTerminalLine(
        "system",
        "Reach out: rakesh@surampalli.dev • LinkedIn: /in/rakeshsurampalli • GitHub: @rakeshsurampalli"
      );
      break;
    case "theme":
      appendDevTerminalLine("system", "Theme controls are locked on the cosmic dark setting.");
      break;
    case "exit":
      appendDevTerminalLine("system", "Closing terminal. See you soon.");
      toggleDevTerminal(false);
      break;
    default:
      appendDevTerminalLine(
        "error",
        `Command "${normalized}" not recognized. Type "help" for available commands.`
      );
      break;
  }
};

if (devToggle) {
  devToggle.addEventListener("click", () => toggleDevTerminal(true));
}

Array.prototype.forEach.call(devTerminalDismiss, (element) => {
  element.addEventListener("click", () => toggleDevTerminal(false));
});

document.addEventListener("keydown", (event) => {
  if (!devTerminal || !devTerminal.classList.contains("is-open")) return;

  if (event.key === "Escape") {
    toggleDevTerminal(false);
    return;
  }

  if (event.key === "Tab") {
    const focusable = getDevTerminalFocusables();
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }
});

if (devTerminalInput) {
  devTerminalInput.addEventListener("keydown", (event) => {
    cancelDevTerminalDemo();
    if (event.key === "Enter") {
      event.preventDefault();
      const value = devTerminalInput.value;
      appendDevTerminalLine("input", value || "");
      handleDevCommand(value);
      devTerminalInput.value = "";
    }
  });
}
