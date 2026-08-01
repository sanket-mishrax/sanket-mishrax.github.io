$(document).ready(function () {
  function togglePublicationBlock($trigger, selector) {
    const $entry = $trigger.closest(".row");
    $entry.find(selector).toggleClass("open");
  }

  function closeOtherPublicationBlocks($trigger, selectors) {
    const $entry = $trigger.closest(".row");
    selectors.forEach(function (selector) {
      $entry.find(selector).removeClass("open");
    });
  }

  // add toggle functionality to abstract, award and bibtex buttons
  $("a.abstract").click(function (event) {
    event.preventDefault();
    closeOtherPublicationBlocks($(this), [".award.hidden", ".bibtex.hidden"]);
    togglePublicationBlock($(this), "div.abstract.hidden");
  });
  $("a.award").click(function (event) {
    event.preventDefault();
    closeOtherPublicationBlocks($(this), ["div.abstract.hidden", ".bibtex.hidden"]);
    togglePublicationBlock($(this), ".award.hidden");
  });
  $("a.bibtex").click(function (event) {
    event.preventDefault();
    closeOtherPublicationBlocks($(this), ["div.abstract.hidden", ".award.hidden"]);
    togglePublicationBlock($(this), ".bibtex.hidden");
  });
  $("a").removeClass("waves-effect waves-light");

  // bootstrap-toc
  if ($("#toc-sidebar").length) {
    // remove related publications years from the TOC
    $(".publications h2").each(function () {
      $(this).attr("data-toc-skip", "");
    });
    var navSelector = "#toc-sidebar";
    var $myNav = $(navSelector);
    Toc.init($myNav);
    $("body").scrollspy({
      target: navSelector,
    });
  }

  // add css to jupyter notebooks
  const cssLink = document.createElement("link");
  cssLink.href = "../css/jupyter.css";
  cssLink.rel = "stylesheet";
  cssLink.type = "text/css";

  let theme = determineComputedTheme();

  $(".jupyter-notebook-iframe-container iframe").each(function () {
    $(this).contents().find("head").append(cssLink);

    if (theme == "dark") {
      $(this).bind("load", function () {
        $(this).contents().find("body").attr({
          "data-jp-theme-light": "false",
          "data-jp-theme-name": "JupyterLab Dark",
        });
      });
    }
  });
});
