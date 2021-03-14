(function() {
  window.addEventListener("pywebviewready", function() {
    while (window.pywebview.api === undefined) {};
    window.pywebview.api.initialize();
  });
  
  document.getElementById("btn-start").addEventListener("click", function(e) {
    if (!this.disabled) {
      if (this.classList.contains("activated")) {
        window.pywebview.api.stopPhantom();
      }
      else {
        var form = document.forms[0];
        window.pywebview.api.runPhantom(form["server-url"].value, form["port-number"].value);
      }
    }
  });
})();