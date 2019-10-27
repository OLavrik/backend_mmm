
let transport = function (data, callback) {
    chrome.extension.sendMessage(data, callback);
};

concerts_mockup = [
{
'img': 'img',
'title': 'большой тур по россии',
'hall': 'Лужники',
'date': '28.10.2019'
},
{
'img': 'img',
'title': 'большой тур по россии',
'hall': 'Лужники',
'date': '28.10.2019'
},
{
'img': 'img',
'title': 'большой тур по россии',
'hall': 'Лужники',
'date': '28.10.2019'
}
]

let wordstatWebAssistantLoad = function ($, window) {

    if (window.location.pathname.search('artist') > 0) {
        if (!($('.tabs_concerts_new').length)) {
            $('.tabs__more').before('<div class="tabs__tab tabs_concerts_new" data-b="926"><a class="link" href="/artist/5324691/concerts">Концерты</a></div>');
        }

        if (window.location.pathname.search('concerts') > 0) {
            if (!($('.tabs__tab_current').length)) {
                $('.tabs_concerts_new').addClass('tabs__tab_current');

                concerts = '<div class="page-artist__subhead"><div class="title title_hover"><span class="title__label">Концерты</span><a href="/artist/5324691/tracks" class="link link_arrow">Все треки</a></div></div><div class="page-artist__tracks_top" data-card="top_tracks">'
                concerts_mockup.forEach(function(e) {
                    concerts += '<div class="track track_basic track_selectable" data-b="1314">'
                    concerts += '<a href="" class="track__cover"> <img src="//avatars.yandex.net/get-music-content/175191/d2210c07.a.5504839-1/50x50" class="album-cover album-cover_size_S" srcset="//avatars.yandex.net/get-music-content/175191/d2210c07.a.5504839-1/100x100 2x"> </a>'
                    concerts += '<div class="track__name"><div class="track__name-wrap"><a href="%" class="track__title link" title="' + e.title + '">' + e.title + '</a> <div class="track__artists"><a href="/artist/5324691" title="' + e.hall + '" class="link ">' + e.hall + '</a></div></div></div>'
                    concerts += '<div class="track__time"><div class="track__nohover">' + e.date + '</div></div>'
                    concerts += '</div>'
                })
                concerts += '</div>'

                $('.page-artist__tabs').after(concerts);
            }
        }

        if (!($('.d-share-popup_after').length)) {
            $('.d-share-popup').after('<div class="track track_basic d-share-popup_after" style="text-align: center;padding-top: 20px; padding-left:40px; padding-right:40px;color: #FFFFFF;vertical-align: middle; width: 400px; background-image: url(\'chrome-extension://dcikkhacpoppgnmbnnebdiafoeccbdoc/images/icons/add.png\')" data-b="1314"></div>');

            countdown(new Date('October 27, 2019 03:24:00'), function(ts) {
                  $('.d-share-popup_after').html('До ближайшего концерта: </br>' + ts.toHTML("strong"));
                },
                countdown.HOURS|countdown.MINUTES|countdown.SECONDS);
        }
    }

    if (window.location.pathname.search('playlists') > 0) {
        if (!($('.page-playlist__sync-button').length)) {
            $('.page-playlist__title_wrapper').after('<a data-modal="#modal" href="#"><div class="d-addition page-playlist__sync-button" data-b="600"><button class="d-button deco-button d-button_rounded d-button_size_L d-button_w-icon d-button_w-icon-centered d-addition__opener" data-b="601" type="button"><span class="d-button-inner deco-button-stylable"><span class="d-button__inner"><span class="d-icon deco-icon d-icon_plus-big" style="opacity: .9;background-image: url(\'chrome-extension://dcikkhacpoppgnmbnnebdiafoeccbdoc/images/icons/export.png\'"></span></span></span></button></div></a>');
        }

    }
 };



exportVK = function($, window) {
    spinner = new Spinner({
  lines: 7, // The number of lines to draw
  length: 38, // The length of each line
  width: 22, // The line thickness
  radius: 45, // The radius of the inner circle
  scale: 1, // Scales overall size of the spinner
  corners: 1, // Corner roundness (0..1)
  color: '#FF0000', // CSS color or array of colors
  fadeColor: 'transparent', // CSS color or array of colors
  speed: 0.5, // Rounds per second
  rotate: 0, // The rotation offset
  animation: 'spinner-line-fade-quick', // The CSS animation name for the lines
  direction: 1, // 1: clockwise, -1: counterclockwise
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  className: 'spinner', // The CSS class to assign to the spinner
  top: '50%', // Top position relative to parent
  left: '50%', // Left position relative to parent
  shadow: '0 0 1px transparent', // Box-shadow for the lines
  position: 'absolute' // Element positioning
}).spin();
    creds = {}
    $('BODY').append(spinner.el)
    chrome.runtime.sendMessage({giveMe: "token"}, function(response) {
    console.log(response.here);
    creds['token'] = response.here;
    });

    chrome.runtime.sendMessage({giveMe: "yandexuid"}, function(response) {
    console.log(response.here);
    creds['yandexuid'] = response.here
    });

    vk_id = console.log(jQuery('.modal_vk_id').value);
    console.log(vk_id)
setTimeout(() => {
    var xhr = new XMLHttpRequest();
var url = "http://35.223.126.78:5000/plsync/";
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var json = JSON.parse(xhr.responseText);
        console.log(json);
    }
};
var data = JSON.stringify({
  "vk_user_id": 541051855,
  "mts_kind": 1022,
  "mts_token": creds["token"],
  "mts_login": "uid-spfxjqf4",
  "mts_yandexuid": creds["yandexuid"],
  "mts_sign": "529900a1e1981a69b08928cff0821ae57895a8bc:1572146433950"
});
xhr.send(data);
}, 1000);

    //Query export here
    setTimeout(() => spinner.stop(), 2000);
}

jQuery(function () {

    /*let config = {
        action: 'check'
    };
    transport(config, function (response) {
        if (response.result) {
            wordstatWebAssistantLoad(jQuery, window, transport);
        } else {
            alert('Пожалуйста, приобретите подписку и перезагрузите страницу для продолжения работы с плагином. ' +
                'Ссылка для приобретения подписки https://chrome.google.com/webstore/detail/wordstat-web-assistant/dcikkhacpoppgnmbnnebdiafoeccbdoc?authuser=2');
        }
    });*/


    jQuery('BODY').prepend('<div class="modal modal-small" data-modal-window id="modal"><a class="close" data-modal-close>x</a><h3 id="modalheader">VK export</h3><p>Откройте аудиозаписи на своей странице ВК на время экспорта</p><input type="text" class="page-playlist__title modal_vk_id" maxlength="89" title="Probide your page ID" value="127001"><button data-modal-ok id="data_export_vk_audio">Export</button><button data-modal-close>Close</button></div>')

    jQuery('#data_export_vk_audio').click(() => exportVK(jQuery, window))
    modals.init();

    wordstatWebAssistantLoad(jQuery, window);
    setInterval(() => wordstatWebAssistantLoad(jQuery, window), 10);
});

// no conflict
jQuery.noConflict();