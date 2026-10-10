(function () {
  const { WA, FREE, REG, PHOTOS, HERO_VIDEO, HERO_POSTER } = window.HK,
    P = window.HK_PRODUCTS,
    DIM = window.HK_IMG,
    IC = window.HK_IC,
    PG = document.body.dataset.page;
  const $ = (i) => document.getElementById(i),
    on = (i, ev, fn) => {
      const e = $(i);
      e && e.addEventListener(ev, fn);
    },
    m = (n) => "₦" + Math.round(n).toLocaleString("en-NG");
  const ic = (n) =>
    `<svg class="i" viewBox="0 0 24 24" aria-hidden="true">${IC[n]}</svg>`;
  const store = {
    get(k, d) {
      try {
        const v = localStorage.getItem(k);
        return v ? JSON.parse(v) : d;
      } catch (e) {
        return d;
      }
    },
    set(k, v) {
      try {
        localStorage.setItem(k, JSON.stringify(v));
      } catch (e) {}
    },
  };
  let cart = store.get("hk-cart", {}),
    fav = store.get("hk-fav", []),
    region = store.get("hk-region", "Lagos");
  if (!REG[region]) region = "Lagos";
  const IMG = "assets/images/";
  const pic = (x, lazy = true) => {
    const n = x.im,
      d = DIM[n],
      s = PHOTOS[x.n] || IMG + n + ".jpg";
    return `<img src="${s}" alt="${x.n}, handmade ${x.kind.toLowerCase()}"${d && !PHOTOS[x.n] ? ` width="${d[0]}" height="${d[1]}"` : ""}${lazy ? ' loading="lazy"' : ""}>`;
  };
  const CATS = window.HK_CATS,
    sizeOf = (x) => (CATS[x.c] || { def: "M" }).def;
  const words = (q) => q.toLowerCase().split(/\s+/).filter(Boolean),
    hay = (x) =>
      (
        x.n +
        " " +
        x.c +
        " " +
        x.d +
        " " +
        (x.tags || "") +
        " " +
        x.kind
      ).toLowerCase();
  const find = (q) => {
    const w = words(q);
    return w.length
      ? P.filter((x) => {
          const h = hay(x);
          return w.every(
            (t) =>
              h.includes(t) ||
              (t.length > 3 && h.includes(t.replace(/s$/, ""))),
          );
        })
      : [];
  };
  const isFav = (id) => fav.indexOf(+id) > -1;
  const pc = (x, add) =>
    `<div class="pcard" data-id="${x.id}" data-href="${x.slug}.html"><div class="pi"><a href="${x.slug}.html" aria-label="${x.n}">${pic(x)}</a>${x.b ? `<span class="bdg">${x.b}</span>` : ""}<button class="hrt" data-h="${x.id}" aria-label="Save ${x.n} to wishlist" aria-pressed="${isFav(x.id)}" type="button">${ic("heart")}</button></div><b><a href="${x.slug}.html">${x.n}</a></b><small>${m(x.p)}</small><div class="st">★★★★★ <span>(${x.rv})</span></div>${add ? `<button class="btn sm alt" data-add="${x.id}" type="button" style="margin-top:6px;align-self:flex-start">Add to cart</button>` : ""}</div>`;
  function toast(t, link) {
    const e = $("ts");
    if (!e) return;
    e.innerHTML = t + (link ? ` <a href="${link[0]}">${link[1]}</a>` : "");
    e.classList.add("on");
    e.classList.toggle("act", !!link);
    clearTimeout(toast.h);
    toast.h = setTimeout(() => e.classList.remove("on"), link ? 2800 : 1600);
  }
  function cnt() {
    let n = 0;
    for (const k in cart) n += cart[k];
    const e = $("cc");
    if (e) e.textContent = n;
  }
  function wcnt() {
    const e = $("wc");
    if (!e) return;
    e.textContent = fav.length;
    e.hidden = !fav.length;
  }
  function syncFav() {
    document
      .querySelectorAll("[data-h]")
      .forEach((b) =>
        b.setAttribute("aria-pressed", isFav(b.getAttribute("data-h"))),
      );
    const l = $("wlab");
    if (l) {
      const id = $("wbtn").getAttribute("data-h");
      l.textContent = isFav(id) ? "Saved to wishlist" : "Save to wishlist";
    }
    wcnt();
  }
  function toggleFav(id) {
    id = +id;
    const i = fav.indexOf(id),
      x = P[id];
    if (i > -1) {
      fav.splice(i, 1);
      toast(`${x.n} removed from your wishlist`);
    } else {
      fav.push(id);
      toast(`${x.n} saved to your wishlist`, [
        "wishlist.html",
        "View wishlist",
      ]);
    }
    store.set("hk-fav", fav);
    syncFav();
    if (PG === "wishlist") renderWish();
  }
  function addc(id, sz) {
    const k = id + "|" + sz;
    cart[k] = (cart[k] || 0) + 1;
    store.set("hk-cart", cart);
    cnt();
    toast("Added to cart", ["cart.html", "View cart"]);
  }
  function renderWish() {
    const g = $("wg");
    if (!g) return;
    const l = fav.map((i) => P[i]).filter(Boolean);
    g.innerHTML = l.map((x) => pc(x, true)).join("");
    $("wempty").hidden = !!l.length;
    $("wact").hidden = !l.length;
    $("wsub").textContent = l.length
      ? `${l.length} saved ${l.length === 1 ? "piece" : "pieces"}. They stay here on this device.`
      : "Pieces you have saved appear here.";
  }
  // ---- region
  function setRegion(v) {
    region = v;
    store.set("hk-region", v);
    ["rg", "rg2"].forEach((i) => {
      const e = $(i);
      if (e) e.value = v;
    });
    if ($("ci")) rcart();
  }
  ["rg", "rg2"].forEach((i) => {
    const e = $(i);
    if (!e) return;
    e.innerHTML = Object.keys(REG)
      .map((r) => `<option>${r}</option>`)
      .join("");
    e.value = region;
    e.addEventListener("change", (ev) => setRegion(ev.target.value));
  });
  // ---- hero (home)
  const HS = [
    {
      eb: "Handmade crochet wear",
      h: "Made by hand.<br>Made for you.",
      p: "From stylish everyday pieces to custom designs, Hookagé brings your crochet dreams to life.",
      a: ["Shop collection", "shop.html"],
      b: ["Create your own", "custom.html"],
      im: "hero",
      alt: "Model in a handmade crochet bucket hat surrounded by colourful yarn strands",
      scr: "Wear your story ♡",
    },
    {
      eb: "Custom crochet",
      h: "Have a design in mind?",
      p: "Send us your sketch. We crochet it to your size and colours.",
      a: ["Start your custom design", "custom.html"],
      b: ["How it works", "faq.html"],
      im: "custom",
      alt: "An orange crochet dress, hat, and bikini laid out flat",
      fr: 1,
    },
    {
      eb: "Beach season",
      h: "Sun, sea, and handmade.",
      p: "Light, breathable crochet for beach days and warm evenings.",
      a: ["Shop beachwear", "beachwear.html"],
      b: ["View all", "shop.html"],
      im: "cat-beachwear",
      alt: "Handmade crochet bikini and beach skirt laid flat",
      fr: 1,
    },
  ];
  let hi = 0,
    ht,
    paused = false;
  function hero() {
    const s = HS[hi],
      e = $("hero"),
      T = hi === 0 ? "h1" : "h2",
      d = DIM[s.im],
      ov = PHOTOS[s.im];
    e.classList.toggle("framed", !!s.fr);
    const med =
      hi === 0 && HERO_VIDEO
        ? `<video ${paused ? "" : "autoplay"} muted loop playsinline preload="metadata" poster="${HERO_POSTER}" aria-label="${s.alt}"><source src="${HERO_VIDEO}" type="video/mp4"></video>`
        : `<img src="${ov || IMG + s.im + ".jpg"}" alt="${s.alt}"${d && !ov ? ` width="${d[0]}" height="${d[1]}"` : ""}${hi === 0 ? ' fetchpriority="high"' : ""}>`;
    e.innerHTML = `<div class="ph">${med}</div>${s.scr ? `<div class="scr" aria-hidden="true">${s.scr}</div>` : ""}<div class="wrap tx"><div class="eb">${s.eb}</div><${T} class="${hi ? "hh" : ""}">${s.h}</${T}><p>${s.p}</p><div class="row"><a class="btn" href="${s.a[1]}">${s.a[0]} ${ic("arrow")}</a><a class="btn alt" href="${s.b[1]}">${s.b[0]} ${ic("arrow")}</a></div></div><button class="arw l" data-hn="-1" aria-label="Previous slide" type="button">‹</button><button class="arw r" data-hn="1" aria-label="Next slide" type="button">›</button><div class="dots" role="group" aria-label="Choose slide">${HS.map((_, i) => `<button type="button" data-hs="${i}" class="${i === hi ? "on" : ""}" aria-label="Slide ${i + 1}"></button>`).join("")}<button class="pz" id="hp" type="button" aria-label="${paused ? "Play" : "Pause"} slideshow">${paused ? "▶" : "❚❚"}</button></div>`;
  }
  function autoHero() {
    clearInterval(ht);
    if (!paused && !matchMedia("(prefers-reduced-motion:reduce)").matches)
      ht = setInterval(() => {
        hi = (hi + 1) % HS.length;
        hero();
      }, 7000);
  }
  if ($("hero")) {
    (function () {
      const h = $("hero");
      let x0 = 0;
      h.addEventListener(
        "touchstart",
        (e) => {
          x0 = e.changedTouches[0].clientX;
        },
        { passive: true },
      );
      h.addEventListener("touchend", (e) => {
        const dx = e.changedTouches[0].clientX - x0;
        if (Math.abs(dx) > 50) {
          hi = (hi + (dx < 0 ? 1 : -1) + HS.length) % HS.length;
          hero();
          autoHero();
        }
      });
    })();
    autoHero();
    $("hero").addEventListener("mouseenter", () => clearInterval(ht));
    $("hero").addEventListener("mouseleave", autoHero);
  }
  on("cl", "click", () => $("cm").scrollBy({ left: -300, behavior: "smooth" }));
  on("cr", "click", () => $("cm").scrollBy({ left: 300, behavior: "smooth" }));
  on("nf", "submit", (e) => {
    e.preventDefault();
    toast(
      $("ne").value.includes("@")
        ? "Thanks for subscribing."
        : "Enter a valid email address.",
    );
  });
  // ---- shop pages: static HTML is already there; JS only handles search + sort
  const SH = $("pg-shop"),
    S = { q: new URLSearchParams(location.search).get("q") || "", o: "pop" };
  function shop() {
    const cat = SH.dataset.cat || "All";
    let l = P.filter((x) => cat === "All" || x.c === cat);
    if (S.q.trim()) {
      const ids = new Set(find(S.q).map((x) => x.id));
      l = l.filter((x) => ids.has(x.id));
    }
    if (S.o === "lo") l.sort((a, b) => a.p - b.p);
    if (S.o === "hi") l.sort((a, b) => b.p - a.p);
    if (S.o === "pop") l.sort((a, b) => b.r - a.r);
    const q = S.q.trim();
    $("rc").textContent = l.length + " pieces" + (q ? ` for “${q}”` : "");
    $("sg").innerHTML = l.length
      ? l.map((x) => pc(x, 1)).join("")
      : '<p class="muted">No matches' +
        (q ? ` for “${q}”` : "") +
        ". Try a different word, like bikini, mesh, checker, or bag.</p>";
    syncFav();
  }
  if (SH && $("sg")) {
    if ($("sq")) $("sq").value = S.q;
    if (S.q) shop();
    on("so", "change", (e) => {
      S.o = e.target.value;
      shop();
    });
    on("sq", "input", (e) => {
      S.q = e.target.value;
      shop();
    });
  }
  // ---- cart
  function rcart() {
    const ks = Object.keys(cart);
    let s = 0,
      h = "";
    ks.forEach((k) => {
      const [id, sz] = k.split("|"),
        x = P[id],
        q = cart[k];
      if (!x) return;
      s += x.p * q;
      h += `<div class="line"><span class="row">${pic(x).replace("<img ", '<img class="thumb" ')}<span><b><a href="${x.slug}.html">${x.n}</a></b><br><small class="muted">${sz} · ${m(x.p)}</small></span></span><span class="row"><button class="btn alt sm" data-q="${k}|-1" aria-label="Remove one" type="button">-</button>${q}<button class="btn alt sm" data-q="${k}|1" aria-label="Add one" type="button">+</button></span></div>`;
    });
    $("ci").innerHTML = ks.length
      ? "<h3>Your cart</h3>" + h
      : '<h3>Your cart is empty</h3><p class="muted">Find something you love in the shop.</p><a class="btn" href="shop.html">Browse the shop</a>';
    const loc = region === "Lagos" || region === "Nigeria, other states",
      d = !ks.length ? 0 : loc && s >= FREE ? 0 : REG[region];
    $("t1").textContent = m(s);
    $("t2").textContent = d ? m(d) : "Free";
    $("t3").textContent = m(s + d);
    cnt();
  }
  on("pay", "click", () => {
    const e = $("ce");
    if (!Object.keys(cart).length) {
      e.textContent = "Add an item to your cart first.";
      return;
    }
    if (
      !$("dn").value.trim() ||
      !$("dp").value.trim() ||
      !$("da").value.trim()
    ) {
      e.textContent = "Enter your name, phone number, and delivery address.";
      return;
    }
    e.textContent = "";
    $("done").textContent = "Order placed. Your order code is HK-1042.";
    cart = {};
    store.set("hk-cart", cart);
    rcart();
  });
  // ---- WhatsApp checkout: builds the order message from the cart and opens WhatsApp
  on("wacheck", "click", () => {
    const e = $("ce"),
      ks = Object.keys(cart).filter((k) => P[k.split("|")[0]]);
    if (!ks.length) {
      e.textContent = "Add an item to your cart first.";
      return;
    }
    const nm = $("dn").value.trim(),
      ph = $("dp").value.trim(),
      ad = $("da").value.trim();
    if (!nm || !ph || !ad) {
      e.textContent = "Enter your name, phone number, and delivery address.";
      return;
    }
    e.textContent = "";
    let s = 0;
    const web = /^https?:$/.test(location.protocol);
    const lines = ks.map((k, i) => {
      const [id, sz] = k.split("|"),
        x = P[id],
        q = cart[k];
      s += x.p * q;
      return (
        `${i + 1}. ${x.n} (${sz}) x${q}: ${m(x.p * q)}` +
        (web ? `\n    ${new URL(x.slug + ".html", location.href).href}` : "")
      );
    });
    const loc = region === "Lagos" || region === "Nigeria, other states",
      d = loc && s >= FREE ? 0 : REG[region];
    const msg = `Hi Hookagé, I'd like to place an order.\n\n*My order*\n${lines.join("\n")}\n\nSubtotal: ${m(s)}\nDelivery (${region}): ${d ? m(d) : "Free"}\n*Total: ${m(s + d)}*\n\n*Delivery details*\nName: ${nm}\nPhone: ${ph}\nAddress: ${ad}\nRegion: ${region}\n\nPlease confirm availability and how to pay. Thank you!`;
    $("wapre").textContent = msg;
    $("wamsg").hidden = false;
    $("wacok").textContent = "";
    window.open(
      "https://wa.me/" + WA + "?text=" + encodeURIComponent(msg),
      "_blank",
      "noopener",
    );
  });
  on("wacopy", "click", () => {
    const t = $("wapre").textContent,
      o = () => {
        $("wacok").textContent = "Copied";
      },
      f = () => {
        $("wacok").textContent = "Select the text above and copy it";
      };
    try {
      navigator.clipboard.writeText(t).then(o, f);
    } catch (x) {
      f();
    }
  });
  // ---- track
  const TS = [
    "Request received",
    "Quote approved",
    "Deposit paid",
    "Crocheting",
    "Quality check",
    "Shipped",
    "Delivered",
  ];
  on("tb", "click", () => {
    const v = $("tc").value.trim().toUpperCase(),
      e = $("te");
    if (v !== "HK-1042") {
      e.textContent = "We couldn't find that code. Check it and try again.";
      $("tl").innerHTML = "";
      return;
    }
    e.textContent = "";
    $("tl").innerHTML = TS.map(
      (t, i) =>
        `<li class="${i < 3 ? "d" : i === 3 ? "c" : ""}">${t}${i === 3 ? " (in progress)" : ""}</li>`,
    ).join("");
  });
  // ---- custom order wizard
  if ($("gar")) {
    const PR = {
      Dress: 75000,
      Top: 38000,
      "Two-piece set": 55000,
      "Cover-up": 60000,
      "Kids set": 40000,
      "Tote bag": 25000,
      Other: 0,
    };
    let g = "",
      step = 1,
      cp = "Sunset";
    $("gar").innerHTML = Object.keys(PR)
      .map(
        (k, i) =>
          `<span><input type="radio" name="g" id="g${i}" value="${k}"><label for="g${i}">${k}</label></span>`,
      )
      .join("");
    $("pl").innerHTML = ["Sunset", "Ocean", "Garden", "Neutral", "Bold brights"]
      .map(
        (k, i) =>
          `<span><input type="radio" name="p" id="p${i}" value="${k}"${i === 0 ? " checked" : ""}><label for="p${i}">${k}</label></span>`,
      )
      .join("");
    const est = () => {
      const s = document.querySelector("input[name=g]:checked");
      g = s ? s.value : "";
      cp = document.querySelector("input[name=p]:checked").value;
      const z = $("sz").value,
        f = $("fb").value;
      $("m1").textContent = g || "Not chosen";
      $("m2").textContent = z || "Not chosen";
      $("m3").textContent = f;
      if (!g) {
        $("es").innerHTML = "&mdash;";
        return;
      }
      if (g === "Other") {
        $("es").textContent = "Quote on request";
        return;
      }
      let p =
        PR[g] + (f === "Wool blend" ? 8000 : f === "Acrylic blend" ? -3000 : 0);
      if (z === "2XL and up") p *= 1.15;
      if (z === "Custom measurements") p *= 1.1;
      $("es").textContent = "From " + m(Math.round(p / 500) * 500);
    };
    const go = (n) => {
      step = n;
      for (let i = 1; i <= 4; i++) $("s" + i).classList.toggle("on", i === n);
      $("pb").style.width = n * 25 + "%";
      $("bk").style.visibility = n === 1 ? "hidden" : "visible";
      $("nx").style.display = n === 4 ? "none" : "inline-flex";
      $("er").textContent = "";
    };
    const prep = () => {
      const ok = $("nm").value.trim() && $("ct").value.trim(),
        w = $("wa"),
        p = $("msg");
      if (!ok) {
        w.style.display = "none";
        p.style.display = "none";
        return;
      }
      const t = `Hi Hookagé, I'd like a custom piece.\n\nPiece: ${g}\nDesign: ${$("ds").value.trim()}${$("rf").value.trim() ? "\nReference: " + $("rf").value.trim() : ""}\nSize: ${$("sz").value}\nYarn: ${$("fb").value}\nColour mood: ${cp}${$("cl").value.trim() ? "\nColours: " + $("cl").value.trim() : ""}${$("dt").value ? "\nNeeded by: " + $("dt").value : ""}\nEstimate shown: ${$("es").textContent}\n\nName: ${$("nm").value.trim()}\nContact: ${$("ct").value.trim()}`;
      p.textContent = t;
      p.style.display = "block";
      w.href = "https://wa.me/" + WA + "?text=" + encodeURIComponent(t);
      w.style.display = "inline-flex";
    };
    $("pg-custom").addEventListener("input", est);
    $("pg-custom").addEventListener("change", est);
    $("bk").addEventListener("click", () => go(step - 1));
    $("nx").addEventListener("click", () => {
      const e = $("er");
      if (step === 1 && !g) {
        e.textContent = "Choose a piece to continue.";
        return;
      }
      if (step === 2 && !$("ds").value.trim()) {
        e.textContent = "Describe your design to continue.";
        return;
      }
      if (step === 3 && !$("sz").value) {
        e.textContent = "Choose a size to continue.";
        return;
      }
      if (step === 3) {
        go(4);
        prep();
        return;
      }
      go(step + 1);
    });
    $("nm").addEventListener("input", prep);
    $("ct").addEventListener("input", prep);
    est();
    go(1);
  }
  // ---- global clicks
  document.addEventListener("click", (e) => {
    let a = e.target.closest("[data-h]");
    if (a) {
      toggleFav(a.getAttribute("data-h"));
      return;
    }
    a = e.target.closest("[data-add]");
    if (a) {
      const i = a.getAttribute("data-add");
      addc(i, sizeOf(P[i]));
      return;
    }
    a = e.target.closest("[data-addp]");
    if (a) {
      const c = document.querySelector("[data-sz].on");
      addc(a.getAttribute("data-addp"), c ? c.getAttribute("data-sz") : "M");
      return;
    }
    a = e.target.closest("[data-sz]");
    if (a) {
      document
        .querySelectorAll("[data-sz]")
        .forEach((b) => b.classList.toggle("on", b === a));
      return;
    }
    a = e.target.closest("[data-q]");
    if (a) {
      const p = a.getAttribute("data-q").split("|"),
        k = p[0] + "|" + p[1];
      cart[k] = (cart[k] || 0) + +p[2];
      if (cart[k] < 1) delete cart[k];
      store.set("hk-cart", cart);
      rcart();
      return;
    }
    a = e.target.closest("[data-hn]");
    if (a) {
      hi = (hi + +a.getAttribute("data-hn") + HS.length) % HS.length;
      hero();
      autoHero();
      return;
    }
    a = e.target.closest("#hp");
    if (a) {
      paused = !paused;
      hero();
      autoHero();
      return;
    }
    a = e.target.closest("[data-hs]");
    if (a) {
      hi = +a.getAttribute("data-hs");
      hero();
      autoHero();
      return;
    }
    a = e.target.closest("#wall");
    if (a) {
      fav.forEach((i) => {
        const k = i + "|" + sizeOf(P[i]);
        cart[k] = (cart[k] || 0) + 1;
      });
      store.set("hk-cart", cart);
      cnt();
      toast("All saved pieces added to your cart", ["cart.html", "View cart"]);
      return;
    }
    a = e.target.closest("#wclr");
    if (a) {
      fav = [];
      store.set("hk-fav", fav);
      syncFav();
      renderWish();
      return;
    }
    a = e.target.closest(".pcard[data-href]");
    if (a && !e.target.closest("a,button"))
      location.href = a.getAttribute("data-href");
  });
  // ---- header search with live suggestions
  function suggest() {
    const q = $("hq").value.trim(),
      u = $("sug");
    if (!q) {
      u.hidden = true;
      u.innerHTML = "";
      return;
    }
    const r = find(q);
    u.innerHTML =
      r
        .slice(0, 6)
        .map(
          (x) =>
            `<li><a href="${x.slug}.html"><img src="${PHOTOS[x.n] || IMG + x.im + ".jpg"}" alt="" width="44" height="55"><span>${x.n}</span><small>${m(x.p)}</small></a></li>`,
        )
        .join("") +
      (r.length
        ? `<li><a class="more" href="shop.html?q=${encodeURIComponent(q)}">See all ${r.length} result${r.length === 1 ? "" : "s"}</a></li>`
        : `<li><a class="more" href="shop.html?q=${encodeURIComponent(q)}">No exact matches. Search the shop for “${q}”</a></li>`);
    u.hidden = false;
  }
  on("hq", "input", suggest);
  on("hq", "keydown", (e) => {
    if (e.key === "Escape") {
      $("sug").hidden = true;
    }
  });
  document.addEventListener("click", (e) => {
    if (!e.target.closest("#sbar,#sb")) {
      const u = $("sug");
      if (u) u.hidden = true;
    }
  });
  // ---- header search, theme, back to top
  on("sb", "click", () => {
    const b = $("sbar"),
      o = b.hidden;
    b.hidden = !o;
    $("sb").setAttribute("aria-expanded", o);
    if (o) $("hq").focus();
  });
  let th = store.get("hk-th", "auto");
  const eff = () =>
    th === "auto"
      ? matchMedia("(prefers-color-scheme:dark)").matches
        ? "dark"
        : "light"
      : th;
  function applyTh() {
    const r = document.documentElement;
    if (th === "auto") r.removeAttribute("data-theme");
    else r.setAttribute("data-theme", th);
    document
      .querySelectorAll("input[name=th]")
      .forEach((i) => (i.checked = i.value === th));
    const d = eff() === "dark",
      t = $("tg");
    if (t) {
      t.textContent = d ? "☀" : "☾";
      t.setAttribute(
        "aria-label",
        d ? "Switch to light mode" : "Switch to dark mode",
      );
      t.setAttribute("aria-pressed", d);
    }
    store.set("hk-th", th);
  }
  on("tg", "click", () => {
    th = eff() === "dark" ? "light" : "dark";
    applyTh();
  });
  document.querySelectorAll("input[name=th]").forEach((i) =>
    i.addEventListener("change", () => {
      th = i.value;
      applyTh();
    }),
  );
  matchMedia("(prefers-color-scheme:dark)").addEventListener &&
    matchMedia("(prefers-color-scheme:dark)").addEventListener(
      "change",
      applyTh,
    );
  on("bt", "click", () => {
    try {
      $("top").scrollIntoView({ block: "start", behavior: "smooth" });
    } catch (e) {
      scrollTo(0, 0);
    }
  });
  addEventListener(
    "scroll",
    () => {
      const b = $("bt");
      b &&
        b.classList.toggle(
          "on",
          (document.scrollingElement || document.documentElement).scrollTop >
            500,
        );
    },
    { passive: true },
  );
  addEventListener("storage", () => {
    cart = store.get("hk-cart", {});
    fav = store.get("hk-fav", []);
    cnt();
    syncFav();
    if (PG === "wishlist") renderWish();
  });
  // ---- opening intro: unveil when the page has loaded and the sequence has played once
  const LD = $("loader");
  if (LD && document.documentElement.classList.contains("splash")) {
    const MIN = 2400,
      MAX = 8000;
    let gone = false;
    const finish = () => {
      if (gone) return;
      gone = true;
      LD.classList.add("done");
      setTimeout(() => {
        LD.remove();
        document.documentElement.classList.remove("splash");
      }, 900);
    };
    const check = () =>
      setTimeout(finish, Math.max(0, MIN - performance.now()));
    document.readyState === "complete"
      ? check()
      : addEventListener("load", check);
    setTimeout(finish, MAX);
  } else if (LD) LD.remove();
  applyTh();
  cnt();
  syncFav();
  if ($("ci")) rcart();
  if (PG === "wishlist") renderWish();
})();

/* Mobile menu: open/close, accordion sub-menus, Esc to close */
(function () {
  var header = document.querySelector("header");
  var btn = document.getElementById("menuBtn");
  var nav = document.getElementById("mainNav");
  if (!header || !btn || !nav) return;
  var mobile = window.matchMedia("(max-width:768px)");

  function setOpen(open) {
    header.classList.toggle("menu-open", open);
    btn.setAttribute("aria-expanded", open);
    btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.documentElement.classList.toggle(
      "menu-lock",
      open && mobile.matches,
    );
  }

  btn.addEventListener("click", function () {
    setOpen(!header.classList.contains("menu-open"));
  });

  nav.addEventListener("click", function (e) {
    var toggle = e.target.closest(".sub-toggle");
    if (toggle) {
      // expand or collapse a sub-menu
      var item = toggle.closest(".dd");
      var open = !item.classList.contains("open");
      item.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open);
      return;
    }
    if (e.target.closest("a")) setOpen(false); // close after choosing a link
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && header.classList.contains("menu-open")) {
      setOpen(false);
      btn.focus();
    }
  });

  document.addEventListener("click", function (e) {
    // tap outside to close
    if (header.classList.contains("menu-open") && !e.target.closest("header"))
      setOpen(false);
  });

  if (mobile.addEventListener) {
    mobile.addEventListener("change", function (e) {
      if (!e.matches) setOpen(false);
    });
  }
})();
