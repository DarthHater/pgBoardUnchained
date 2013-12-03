jQuery(document).ready(function(){
  function quote_post(id) {
    var info = $('#post_'+id+'_info .postinfo').text();
    var body = jQuery.trim($('#post_'+id+'_body .postbody').text());
    $('#body').val($('#body').val()+'[quote]'+info+'\n'+body+'[/quote]\n\n');
  };
});

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-18237147-1']);
_gaq.push(['_setDomainName', 'none']);
_gaq.push(['_setAllowLinker', true]);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();