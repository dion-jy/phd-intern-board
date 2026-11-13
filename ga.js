// Google Analytics 4. Empty GA_ID means nothing loads and nothing is sent.
// Visitors in the EEA, the UK and Switzerland start with every storage denied
// (Consent Mode v2), so no analytics cookie is set there until consent is given;
// elsewhere it runs as normal. Outbound clicks to employer pages are counted by
// GA4's enhanced measurement, which is on by default for a web stream.
(function () {
  var GA_ID = "G-QY2ZTXHF4C";
  if (!GA_ID) return;
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("consent", "default", {
    ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied",
    analytics_storage: "denied",
    region: ["AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR","HU","IS",
             "IE","IT","LV","LI","LT","LU","MT","NL","NO","PL","PT","RO","SK","SI",
             "ES","SE","GB","CH"]
  });
  gtag("js", new Date());
  gtag("config", GA_ID);
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
  document.head.appendChild(s);
})();
