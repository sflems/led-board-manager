if (typeof jQuery !== 'undefined' || typeof(django.jQuery) !== 'undefined') {
(function($){
  if (typeof($.fn.JSONView) !== 'undefined') return;
  !function(e){var n,t,l,r;return l=function(){function e(e){null==e&&(e={}),this.options=e}return e.prototype.htmlEncode=function(e){return null!==e?e.toString().replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/</g,"&lt;").replace(/>/g,"&gt;"):""},e.prototype.jsString=function(e){return e=JSON.stringify(e).slice(1,-1),this.htmlEncode(e)},e.prototype.decorateWithSpan=function(e,n){return'<span class="'+n+'">'+this.htmlEncode(e)+"</span>"},e.prototype.valueToHTML=function(e,n){var t;return null==n&&(n=0),t=Object.prototype.toString.call(e).match(/\s(.+)]/)[1].toLowerCase(),this[""+t+"ToHTML"].call(this,e,n)},e.prototype.nullToHTML=function(e){return this.decorateWithSpan("null","null")},e.prototype.numberToHTML=function(e){return this.decorateWithSpan(e,"num")},e.prototype.stringToHTML=function(e){var n,t;return/^(http|https|file):\/\/[^\s]+$/i.test(e)?'<a href="'+this.htmlEncode(e)+'"><span class="q">"</span>'+this.jsString(e)+'<span class="q">"</span></a>':(n="",e=this.jsString(e),this.options.nl2br&&(t=/([^>\\r\\n]?)(\\r\\n|\\n\\r|\\r|\\n)/g,t.test(e)&&(n=" multiline",e=(e+"").replace(t,"$1<br />"))),'<span class="string'+n+'">"'+e+'"</span>')},e.prototype.booleanToHTML=function(e){return this.decorateWithSpan(e,"bool")},e.prototype.arrayToHTML=function(e,n){var t,l,r,o,s,i,a,p;for(null==n&&(n=0),l=!1,s="",o=e.length,r=a=0,p=e.length;p>a;r=++a)i=e[r],l=!0,s+="<li>"+this.valueToHTML(i,n+1),o>1&&(s+=","),s+="</li>",o--;return l?(t=0===n?"":" collapsible",'[<ul class="array level'+n+t+'">'+s+"</ul>]"):"[ ]"},e.prototype.objectToHTML=function(e,n){var t,l,r,o,s,i,a;null==n&&(n=0),l=!1,s="",o=0;for(i in e)o++;for(i in e)a=e[i],l=!0,r=this.options.escape?this.jsString(i):i,s+='<li><span class="prop"><span class="q">"</span>'+r+'<span class="q">"</span></span>: '+this.valueToHTML(a,n+1),o>1&&(s+=","),s+="</li>",o--;return l?(t=0===n?"":" collapsible",'{<ul class="obj level'+n+t+'">'+s+"</ul>}"):"{ }"},e.prototype.jsonToHTML=function(e){return'<div class="jsonview">'+this.valueToHTML(e)+"</div>"},e}(),"undefined"!=typeof module&&null!==module&&(module.exports=l),t=function(){function e(){}return e.bindEvent=function(e,n){var t;return t=document.createElement("div"),t.className="collapser",t.innerHTML=n.collapsed?"+":"-",t.addEventListener("click",function(e){return function(t){return e.toggle(t.target,n)}}(this)),e.insertBefore(t,e.firstChild),n.collapsed?this.collapse(t):void 0},e.expand=function(e){var n,t;return t=this.collapseTarget(e),""!==t.style.display?(n=t.parentNode.getElementsByClassName("ellipsis")[0],t.parentNode.removeChild(n),t.style.display="",e.innerHTML="-"):void 0},e.collapse=function(e){var n,t;return t=this.collapseTarget(e),"none"!==t.style.display?(t.style.display="none",n=document.createElement("span"),n.className="ellipsis",n.innerHTML=" &hellip; ",t.parentNode.insertBefore(n,t),e.innerHTML="+"):void 0},e.toggle=function(e,n){var t,l,r,o,s,i;if(null==n&&(n={}),r=this.collapseTarget(e),t="none"===r.style.display?"expand":"collapse",n.recursive_collapser){for(l=e.parentNode.getElementsByClassName("collapser"),i=[],o=0,s=l.length;s>o;o++)e=l[o],i.push(this[t](e));return i}return this[t](e)},e.collapseTarget=function(e){var n,t;return t=e.parentNode.getElementsByClassName("collapsible"),t.length?n=t[0]:void 0},e}(),n=e,r={collapse:function(e){return"-"===e.innerHTML?t.collapse(e):void 0},expand:function(e){return"+"===e.innerHTML?t.expand(e):void 0},toggle:function(e){return t.toggle(e)}},n.fn.JSONView=function(){var e,o,s,i,a,p,c;return e=arguments,null!=r[e[0]]?(a=e[0],this.each(function(){var t,l;return t=n(this),null!=e[1]?(l=e[1],t.find(".jsonview .collapsible.level"+l).siblings(".collapser").each(function(){return r[a](this)})):t.find(".jsonview > ul > li .collapsible").siblings(".collapser").each(function(){return r[a](this)})})):(i=e[0],p=e[1]||{},o={collapsed:!1,nl2br:!1,recursive_collapser:!1,escape:!0},p=n.extend(o,p),s=new l({nl2br:p.nl2br,escape:p.escape}),"[object String]"===Object.prototype.toString.call(i)&&(i=JSON.parse(i)),c=s.jsonToHTML(i),this.each(function(){var e,l,r,o,s,i;for(e=n(this),e.html(c),r=e[0].getElementsByClassName("collapsible"),i=[],o=0,s=r.length;s>o;o++)l=r[o],"LI"===l.parentNode.nodeName?i.push(t.bindEvent(l.parentNode,p)):i.push(void 0);return i}))}}($);

$( document ).ready(function() {

$('button.parseraw').click(function(e){
  var widget = $(e.target).closest('.jsonwidget');
  var rawarea = widget.find('textarea');
  var parsedarea = widget.find('div.parsed');
  if ($(e.target).text() === 'Show parsed') {
    var validjson = true;
    try {
        JSON.parse(rawarea.val());
    } catch (e) {
      validjson = false;
    }
    if (validjson) {
      rawarea.hide();
      widget.find('.parsed').show();
      parsedarea.JSONView(rawarea.val(), {strict: true}).css({
        overflow: "auto",
        resize: "both"
      });
      $(e.target).text('Show raw');
    } else {
      // invalid json
      window.alert('Enter valid JSON.');
    }

  } else {
    // Clicked Show raw
    rawarea.val(JSON.stringify(JSON.parse(rawarea.val()),null,2));
    widget.find('textarea').show();
    widget.find('.parsed').hide();
    $(e.target).text('Show parsed');
  }
});
$('button.parsed').click(function(e){
  var widget = $(e.target).closest('.jsonwidget');
  var parsedarea = widget.find('div.parsed');
  if ($(e.target).text() === 'Collapse all') {
    parsedarea.JSONView('collapse');
  } else {
    parsedarea.JSONView('expand');
  }
});

$('.jsonwidget').each(function(i) {
  if ($(this).attr('data-initial') == 'parsed') {
    $(this).find('button.parseraw').click();
  }
});

});
})((typeof jQuery !== 'undefined') ? jQuery : django.jQuery);
} else {
  throw new Error('django-prettyjson requires jQuery');
}
