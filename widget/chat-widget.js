/* ====================================
   CHAT WIDGET — chat-widget.js
   ====================================
   Vanilla JS · Appelle l'API RAG /ask
   Usage : <script src="chat-widget.js" data-api="https://your-api-url"></script>
*/

(function () {
  "use strict";

  // ---- ÉTAPE 1 : Configuration ----

  var scriptTag = document.querySelector('script[data-api]');
  var API_URL = scriptTag ? scriptTag.getAttribute("data-api") : "http://localhost:8000";

  // ---- ÉTAPE 2 : Créer le DOM ----

  function buildWidget() {
    var toggle = document.createElement("button");
    toggle.className = "chat-widget__toggle";
    toggle.setAttribute("aria-label", "Ouvrir l'assistant IA");
    toggle.innerHTML = "&#128172;"; // speech balloon

    var panel = document.createElement("div");
    panel.className = "chat-widget__panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "Assistant IA");
    panel.innerHTML =
      '<header class="chat-widget__header">' +
        '<h3 class="chat-widget__title">Assistant IA</h3>' +
        '<button class="chat-widget__close" aria-label="Fermer">&times;</button>' +
      "</header>" +
      '<div class="chat-widget__messages">' +
        '<p class="chat-widget__welcome">' +
          "Bonjour ! Je suis l'assistant IA d'Amazigh.<br>" +
          "Posez-moi une question sur son parcours, ses comp\u00e9tences ou ses projets." +
        "</p>" +
      "</div>" +
      '<div class="chat-widget__typing">' +
        '<span class="chat-widget__dot"></span>' +
        '<span class="chat-widget__dot"></span>' +
        '<span class="chat-widget__dot"></span>' +
      "</div>" +
      '<form class="chat-widget__form">' +
        '<input class="chat-widget__input" type="text" placeholder="Votre question\u2026" autocomplete="off" required minlength="3" maxlength="500">' +
        '<button class="chat-widget__send" type="submit">Envoyer</button>' +
      "</form>";

    document.body.appendChild(toggle);
    document.body.appendChild(panel);

    return {
      toggle: toggle,
      panel: panel,
      close: panel.querySelector(".chat-widget__close"),
      messages: panel.querySelector(".chat-widget__messages"),
      typing: panel.querySelector(".chat-widget__typing"),
      form: panel.querySelector(".chat-widget__form"),
      input: panel.querySelector(".chat-widget__input"),
      send: panel.querySelector(".chat-widget__send"),
    };
  }

  // ---- ÉTAPE 3 : Logique ----

  function initWidget() {
    var el = buildWidget();
    var isOpen = false;

    function togglePanel() {
      isOpen = !isOpen;
      el.panel.classList.toggle("chat-widget__panel--open", isOpen);
      el.toggle.classList.toggle("chat-widget__toggle--hidden", isOpen);
      if (isOpen) {
        el.input.focus();
      }
    }

    function addMessage(text, type) {
      // Remove welcome message on first interaction
      var welcome = el.messages.querySelector(".chat-widget__welcome");
      if (welcome) welcome.remove();

      var msg = document.createElement("div");
      msg.className = "chat-widget__message chat-widget__message--" + type;
      msg.textContent = text;
      el.messages.appendChild(msg);
      el.messages.scrollTop = el.messages.scrollHeight;
      return msg;
    }

    function addSources(container, sources) {
      if (!sources || sources.length === 0) return;

      var wrapper = document.createElement("div");
      wrapper.className = "chat-widget__sources";

      var title = document.createElement("div");
      title.className = "chat-widget__sources-title";
      title.textContent = "Sources :";
      wrapper.appendChild(title);

      sources.forEach(function (s) {
        var line = document.createElement("div");
        line.className = "chat-widget__source";
        var label = s.file;
        if (s.page && s.page !== "?") {
          label += " (p." + s.page + ")";
        }
        line.textContent = label;
        wrapper.appendChild(line);
      });

      container.appendChild(wrapper);
    }

    function showTyping() {
      el.typing.classList.add("chat-widget__typing--visible");
      el.messages.scrollTop = el.messages.scrollHeight;
    }

    function hideTyping() {
      el.typing.classList.remove("chat-widget__typing--visible");
    }

    function setLoading(state) {
      el.send.disabled = state;
      el.input.disabled = state;
      if (state) showTyping();
      else hideTyping();
    }

    function sendMessage(question) {
      addMessage(question, "user");
      setLoading(true);

      fetch(API_URL + "/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question }),
      })
        .then(function (res) {
          if (res.status === 429) {
            throw new Error("Trop de requ\u00eates. R\u00e9essayez dans une minute.");
          }
          if (!res.ok) {
            throw new Error("Erreur serveur. R\u00e9essayez plus tard.");
          }
          return res.json();
        })
        .then(function (data) {
          setLoading(false);
          var botMsg = addMessage(data.answer, "bot");
          addSources(botMsg, data.sources);
        })
        .catch(function (err) {
          setLoading(false);
          addMessage(err.message || "Impossible de contacter l'assistant.", "error");
        });
    }

    // ---- ÉTAPE 4 : Events ----

    el.toggle.addEventListener("click", togglePanel);
    el.close.addEventListener("click", togglePanel);

    el.form.addEventListener("submit", function (e) {
      e.preventDefault();
      var question = el.input.value.trim();
      if (question.length < 3) return;
      el.input.value = "";
      sendMessage(question);
    });

    // Escape to close
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen) {
        togglePanel();
      }
    });
  }

  // ---- ÉTAPE 5 : Lancement ----

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initWidget);
  } else {
    initWidget();
  }
})();
