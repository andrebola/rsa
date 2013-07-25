

/* Text Fader
================================================== */

if ($('#words').length) {

    jQuery(function($) {

        var data = {

            words: [{
                review: "Y"
            }, {
                review: "FaceBook"
            }, {
                review: "Twitter"
            }, {
                review: "[this loops.]"
            }]

        };

        $.each(data.words, function(i, itemData) {
            var p = $('<strong>').text(itemData.review);
            if (i == 0) p.addClass('active');
            else p.css({
                opacity: 0.0
            });
            $('#words').append(p);
        });

        function nextWord() {
            var $active = $('#words strong.active');
            if ($active.length == 0) $active = $('#words strong:last');
            var $next = $active.next().length ? $active.next() : $('#words strong:first');

            $active.removeClass('active').animate({
                opacity: 0.0
            }, 1000, function() {
                $active.hide();
                $next.show().addClass('active').animate({
                    opacity: 1.0
                }, 1000);
            });
        }

        setInterval(nextWord, 5000);

    });

};





/* Contact Form Widget
================================================== */

if ($('#contact').is(":visible")) {

    $("#contact button").click(function() {

        var name = $("#contactname").val();
        var message = $("#contactmessage").val();
        var email = $("#contactemail").val();
        var emailReg = /^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,4}(\.[a-zA-Z]{2,3})?(\.[a-zA-Z]{2,3})?$/;

        // client-side validation
        if (emailReg.test(email) == false) {
            var emailValidation = false;
            $('#contactemail').addClass("error");
        } else $('#contactemail').removeClass("error");

        if (name.length < 1) {
            var nameValidation = false;
            $('#contactname').addClass("error");
        } else $('#contactname').removeClass("error");

        if (message.length < 1) {
            var messageValidation = false;
            $('#contactmessage').addClass("error");
        } else $('#contactmessage').removeClass("error");

        if ((nameValidation == false) || (emailValidation == false) || (messageValidation == false)) return false;

        $.ajax({
            type: "post",
            dataType: "json",
            url: "send-email.php",
            data: $("#contact").serialize(),
            success: function(data) {

                $('.form').html('<p class="success">Email sent. Thank you.</p>');

            }
        });
        return false;
    });

};


/* Misc tidbits. Mostly fixes.
================================================== */

/*! http://mths.be/placeholder v2.0.7 by @mathias */;
(function(f, h, $) {
    var a = 'placeholder' in h.createElement('input'),
        d = 'placeholder' in h.createElement('textarea'),
        i = $.fn,
        c = $.valHooks,
        k, j;
    if (a && d) {
        j = i.placeholder = function() {
            return this
        };
        j.input = j.textarea = true
    } else {
        j = i.placeholder = function() {
            var l = this;
            l.filter((a ? 'textarea' : ':input') + '[placeholder]').not('.placeholder').bind({
                'focus.placeholder': b,
                'blur.placeholder': e
            }).data('placeholder-enabled', true).trigger('blur.placeholder');
            return l
        };
        j.input = a;
        j.textarea = d;
        k = {
            get: function(m) {
                var l = $(m);
                return l.data('placeholder-enabled') && l.hasClass('placeholder') ? '' : m.value
            },
            set: function(m, n) {
                var l = $(m);
                if (!l.data('placeholder-enabled')) {
                    return m.value = n
                }
                if (n == '') {
                    m.value = n;
                    if (m != h.activeElement) {
                        e.call(m)
                    }
                } else {
                    if (l.hasClass('placeholder')) {
                        b.call(m, true, n) || (m.value = n)
                    } else {
                        m.value = n
                    }
                }
                return l
            }
        };
        a || (c.input = k);
        d || (c.textarea = k);
        $(function() {
            $(h).delegate('form', 'submit.placeholder', function() {
                var l = $('.placeholder', this).each(b);
                setTimeout(function() {
                    l.each(e)
                }, 10)
            })
        });
        $(f).bind('beforeunload.placeholder', function() {
            $('.placeholder').each(function() {
                this.value = ''
            })
        })
    }
    function g(m) {
        var l = {}, n = /^jQuery\d+$/;
        $.each(m.attributes, function(p, o) {
            if (o.specified && !n.test(o.name)) {
                l[o.name] = o.value
            }
        });
        return l
    }
    function b(m, n) {
        var l = this,
            o = $(l);
        if (l.value == o.attr('placeholder') && o.hasClass('placeholder')) {
            if (o.data('placeholder-password')) {
                o = o.hide().next().show().attr('id', o.removeAttr('id').data('placeholder-id'));
                if (m === true) {
                    return o[0].value = n
                }
                o.focus()
            } else {
                l.value = '';
                o.removeClass('placeholder');
                l == h.activeElement && l.select()
            }
        }
    }
    function e() {
        var q, l = this,
            p = $(l),
            m = p,
            o = this.id;
        if (l.value == '') {
            if (l.type == 'password') {
                if (!p.data('placeholder-textinput')) {
                    try {
                        q = p.clone().attr({
                            type: 'text'
                        })
                    } catch (n) {
                        q = $('<input>').attr($.extend(g(this), {
                            type: 'text'
                        }))
                    }
                    q.removeAttr('name').data({
                        'placeholder-password': true,
                        'placeholder-id': o
                    }).bind('focus.placeholder', b);
                    p.data({
                        'placeholder-textinput': q,
                        'placeholder-id': o
                    }).before(q)
                }
                p = p.removeAttr('id').hide().prev().attr('id', o).show()
            }
            p.addClass('placeholder');
            p[0].value = p.attr('placeholder')
        } else {
            p.removeClass('placeholder')
        }
    }
}(this, document, jQuery));

function initialize_popup(proy) {
        
  
   $.get('/perfil-pro/'+proy+'/',{},         
        function(resp){
        
         $('#all_popus .pop_content').html(resp);
         $('#all_popus').css('display','table');
         $('#all_popus .center_popup').css('display','')
         var position_top = $(document).scrollTop();
         $('#all_popus').css('top',position_top);
      
          selected = $('#all_popus').find('.go_invite');
          selected.css('display','inline-block');
          var h_screen = $(window).height() -30;
         selected.find('.viewport').css('height', h_screen-100);
         selected.find('.wait .cont').css('height', h_screen-100);
         selected.css('display','inline-block');
         var alto = $(document).height()
        
        $('body').css('overflow-y','hidden');
        $('#popupbg').css('height',alto);
        $('#popupbg').css('display','block');
        
        // $('#all_popus').find('.scroll_viewvid').tinyscrollbar();
        
     });
}
function close_popup(){
          $('#all_popus').css('display','none');
          $('#popupbg').css('display','none');
          $('body').css('overflow-y','auto');
          $('#playing_video').attr('src','')
          $('#all_popus .pop_content').parent().parent().parent().css('display','none')
  }
$('.popupbox').click(function(e){
    e.stopPropagation();
});
$(document).click(function(e){
    close_popup();
});
$('.proy').live('click',function(e){
        
    initialize_popup($(this).attr('proy'));
    e.stopPropagation();
    return false;
});


$('.submit_login').live('click',function(e){

    $('#login_form').submit()
      
    });

$('#login').live('click',function(e){
        
     $.get('/login/',{},         
        function(resp){
        
         $('#all_popus .pop_content').html(resp);
         
        
         $('#all_popus').css('display','table');
         $('#all_popus .center_popup').css('display','')
         var position_top = $(document).scrollTop();
         $('#all_popus').css('top',position_top);
      
          selected = $('#all_popus').find('.go_invite');
          selected.css('display','inline-block');
          var h_screen = $(window).height() -30;
         selected.find('.viewport').css('height', h_screen-100);
         selected.find('.wait .cont').css('height', h_screen-100);
         selected.css('display','inline-block');
         var alto = $(document).height()
        
        $('body').css('overflow-y','hidden');
        $('#popupbg').css('height',alto);
        $('#popupbg').css('display','block');
        
        // $('#all_popus').find('.scroll_viewvid').tinyscrollbar();
        
     });
    
    
    e.stopPropagation();
});

function add_proyect_to_template(resp) {
    
    obj = jQuery.parseJSON(resp);
        var html='';
        for (i=0 ; i< obj.length; i++) {   
        html+='<li><a proy="'+obj[i].id+'"class="proy" href="/perfil-pro/'+obj[i].id+'"><img style="margin-bottom: 30px;" width="300px" height="200px" src="'+obj[i].avatar+'"><p><strong>'+obj[i].nombre+'</strong></p></a></li>';
        if (!obj.length<1){$('ul.features').attr('lastid',obj[i].lastid);}    
        }            
    return html;
}

function get_proyectos(button) {
    var obj;
    if (button.attr('id')=='prev') {
        var id_proy='';
    
        if (!$('ul.features li').length >= 1) id_proy=$('ul.features').attr('lastid');
        else id_proy=$('ul.features li:first a').attr('proy');
        
        $.get('/ajax_proyectos/?pais='+$('#id_paises').find(":selected").val()+'&firstid='+id_proy,{},         
        function(resp){
            if (resp) {
                
            
            html=add_proyect_to_template(resp);
            if(html!='') {
               
                $('ul.features').html('');
                $('ul.features').prepend(html);
            }else
            $('ul.features').prepend(html);
            }
        });return false;
    }
    else
    {
        //aler($('ul.features li').last());
        $.get('/ajax_proyectos/?pais='+$('#id_paises').find(":selected").val()+'&lastid='+$('ul.features li').last().find('a').attr('proy'),{},            
        function(resp){
            if (resp) {
        html=add_proyect_to_template(resp);
          if (html!='') {
            $('ul.features').html('');
            $('ul.features').prepend(html);
        }else
        $('ul.features').prepend(html);
            
        }
        });return false;    
    }
}
$('button.nextprev').live('click',function(e){			      
    
    get_proyectos($(this));
   
});

$(document).ready(function() {
    $('input, textarea').placeholder();
    
  
    $("#id_paises").change(function(){
        var pais=$(this).find(":selected").val();
          $.get('/ajax_proyectos/?lastid=0&pais='+pais,{},            
        function(resp){
            if (resp) {
            html=add_proyect_to_template(resp);
            $('ul.features').html(html);
         }else
         {
            $('ul.features').html('');
         }
         
        });return false; 
    })
    
    
    $.get('/ajax_proyectos/?lastid=0&pais='+$('#id_paises').find(":selected").val(),{},            
        function(resp){
            if (resp) {
        html=add_proyect_to_template(resp);
          if (html!='') {
            $('ul.features').html('');
            $('ul.features').prepend(html);
        }else
        $('ul.features').prepend(html);
    }
        });return false; 
    
}); 