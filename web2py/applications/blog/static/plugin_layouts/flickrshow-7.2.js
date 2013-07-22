(function() {
  /*
   *  @package    Flickrshow
   *  @subpackage Javascript
   *  @author     Ben Sekulowicz-Barclay
   *  @version    7.2
   *  
   *  Flickrshow is a Beseku thing licensed under a Creative Commons Attribution 3.0 
   *  Unported License. For more information visit http://www.flickrshow.co.uk.
   */  var flickrshow;
  var __hasProp = Object.prototype.hasOwnProperty;
  flickrshow = function(target, settings) {
    var key, value, _;
    if (!this instanceof flickrshow) {
      return new flickrshow(target, settings);
    }
    _ = this;
    _.addEvent = function(obj, type, fn) {
      if ((obj != null ? obj.addEventListener : void 0) != null) {
        return obj != null ? obj.addEventListener(type, fn, false) : void 0;
      } else if ((obj != null ? obj.attachEvent : void 0) != null) {
        obj['e' + type + fn] = fn;
        obj[type + fn] = function() {
          return obj['e' + type + fn](window.event);
        };
        return obj != null ? obj.attachEvent('on' + type, obj[type + fn]) : void 0;
      }
    };
    _.addUrl = function() {
      var key, parameters, url, value;
      parameters = {
        api_key: '6cb7449543a9595800bc0c365223a4e8',
        extras: 'url_s,url_m,url_z,url_l',
        format: 'json',
        jsoncallback: 'flickrshow_jsonp_' + _.constants.random,
        page: _.settings.page,
        per_page: _.settings.per_page
      };
      if (_.settings.licence != null) {
        parameters.license = _.settings.licence;
      }
      if (_.settings.license != null) {
        parameters.license = _.settings.license;
      }
      if (_.settings.gallery != null) {
        parameters.method = 'flickr.galleries.getPhotos';
        parameters.gallery_id = _.settings.gallery;
      } else if (_.settings.group != null) {
        parameters.method = 'flickr.groups.pools.getPhotos';
        parameters.group_id = _.settings.group;
      } else if (_.settings.set != null) {
        parameters.method = 'flickr.photosets.getPhotos';
        parameters.photoset_id = _.settings.set;
      } else if (_.settings.person != null) {
        parameters.method = 'flickr.people.getPhotosOf';
        parameters.user_id = _.settings.person;
      } else if ((_.settings.tags != null) || (_.settings.user != null)) {
        parameters.method = 'flickr.photos.search';
        if (_.settings.tags != null) {
          parameters.tags = _.settings.tags;
        }
        if (_.settings.user != null) {
          parameters.user_id = _.settings.user;
        }
      } else {
        parameters.method = 'flickr.photos.getRecent';
      }
      url = 'http://api.flickr.com/services/rest/?';
      for (key in parameters) {
        if (!__hasProp.call(parameters, key)) continue;
        value = parameters[key];
        url += key + '=' + value + '&';
      }
      return url;
    };
    _.animate = function(element, property, endValue, speed, identifier) {
      var execute;
      if (_.constants.intervals[identifier] != null) {
        window.clearInterval(_.constants.intervals[identifier]);
      }
      execute = function() {
        var currentValue, newValue;
        currentValue = Math.round(element.style[property].replace(/([a-zA-Z]{2})$/, ''));
        newValue = Math.round(endValue - currentValue);
        if ((Math.abs(newValue)) > 1) {
          return element.style[property] = Math.floor(currentValue + (newValue / 2)) + 'px';
        } else {
          element.style[property] = endValue + 'px';
          return window.clearInterval(_.constants.intervals[identifier]);
        }
      };
      _.constants.intervals[identifier] = window.setInterval(execute, speed / 1.5);
    };
    _.onClickLeft = function() {
      if (_.constants.isLoading === true) {
        return;
      }
      _.constants.imageCurrent = _.constants.imageCurrent - 1 < 0 ? _.constants.imageTotal - 1 : _.constants.imageCurrent - 1;
      _.animate(_.elements.images, 'left', '-' + (_.constants.imageCurrent * _.elements.target.offsetWidth), _.constants.speed, 'i');
      _.showTitle();
      if (typeof _.settings.onMove === 'function') {
        _.settings.onMove(_.elements.images.childNodes[_.constants.imageCurrent].childNodes[0]);
      }
    };
    _.onClickPlay = function() {
      var execute;
      if (_.constants.isPlaying === false) {
        _.constants.isPlaying = true;
        _.elements.buttons.childNodes[2].style.backgroundImage = 'url(' + _.constants.img_url + 'static/images/is.png)';
        execute = function() {
          return _.onClickRight();
        };
        _.constants.intervals['playing'] = window.setInterval(execute, _.settings.interval);
        if (typeof _.settings.onPlay === 'function') {
          _.settings.onPlay();
        }
      } else {
        _.constants.isPlaying = false;
        _.elements.buttons.childNodes[2].style.backgroundImage = 'url(' + _.constants.img_url + 'static/images/ip.png)';
        window.clearInterval(_.constants.intervals['playing']);
        if (typeof _.settings.onPause === 'function') {
          _.settings.onPause(_.elements.images.childNodes[_.constants.imageCurrent].childNodes[0]);
        }
      }
    };
    _.onClickRight = function() {
      if (_.constants.isLoading === true) {
        return;
      }
      _.constants.imageCurrent = (_.constants.imageCurrent + 2) > _.constants.imageTotal ? 0 : _.constants.imageCurrent + 1;
      _.animate(_.elements.images, 'left', '-' + (_.constants.imageCurrent * _.elements.target.offsetWidth), _.constants.speed, 'i');
      _.showTitle();
      if (typeof _.settings.onMove === 'function') {
        _.settings.onMove(_.elements.images.childNodes[_.constants.imageCurrent].childNodes[0]);
      }
    };
    _.onLoadImage = function(event) {
      var ch, cw, img, nh, nw, percentLoaded;
      img = event.srcElement || event.target;
      ch = img.offsetHeight;
      cw = img.offsetWidth;
      if (cw > ch) {
        nw = Math.ceil(_.elements.target.offsetWidth + (_.elements.target.offsetHeight / 100));
        nh = Math.ceil((nw / cw) * ch);
      } else {
        nh = Math.ceil(_.elements.target.offsetHeight + (_.elements.target.offsetHeight / 100));
        nw = Math.ceil((nh / ch) * cw);
      }
      img.style.height = nh + 'px';
      img.style.left = Math.round((_.elements.target.offsetWidth - nw) / 2) + 'px';
      img.style.position = 'absolute';
      img.style.top = Math.round((_.elements.target.offsetHeight - nh) / 2) + 'px';
      img.style.width = nw + 'px';
      _.constants.imageLoaded = _.constants.imageLoaded + 1;
      percentLoaded = Math.round((_.constants.imageLoaded / _.constants.imageTotal) * 240);
      _.animate(_.elements.loading.childNodes[0], 'width', (percentLoaded <= 36 ? 36 : percentLoaded), 'loading');
      if (_.constants.imageLoaded === _.constants.imageTotal) {
        _.showTitle();
        _.elements.container.removeChild(_.elements.loading);
        _.elements.images.style.visibility = 'visible';
        _.constants.isLoading = false;
        if (_.settings.autoplay === true) {
          _.onClickPlay();
        }
        if (typeof _.settings.onLoad === 'function') {
          _.settings.onLoad();
        }
      }
    };
    _.onLoadJson = function(event) {
      var areaM, areaS, areaT, areaZ, i, img, li, photo, _len, _len2, _ref, _ref2;
      _.elements.script.parentNode.removeChild(_.elements.script);
      if ((event.photoset != null)) {
        _ref = event.photoset.photo;
        for (i = 0, _len = _ref.length; i < _len; i++) {
          photo = _ref[i];
          photo.owner = event.photoset.owner;
        }
        event.photos = event.photoset;
      }
      if (((event.stat != null) && event.stat === 'fail') || !event.photos) {
        throw 'Flickrshow: ' + (event.message || 'There was an unknown error with the data returned by Flickr');
      }
      _.constants.imageTotal = event.photos.photo.length;
      _ref2 = event.photos.photo;
      for (i = 0, _len2 = _ref2.length; i < _len2; i++) {
        photo = _ref2[i];
        img = document.createElement('img');
        img.setAttribute('data-flickr-title', photo.title);
        img.setAttribute('data-flickr-photo_id', photo.id);
        img.setAttribute('data-flickr-owner', photo.owner);
        img.setAttribute('rel', i);
        img.style.cursor = 'pointer';
        img.style.display = 'block';
        img.style.margin = '0';
        img.style.padding = '0';
        areaT = _.elements.target.offsetHeight * _.elements.target.offsetWidth;
        areaZ = photo.height_z * photo.width_z;
        areaM = photo.height_m * photo.width_m;
        areaS = photo.height_s * photo.width_s;
        if (!photo.url_m) {
          photo.url_m = photo.url_s;
        }
        if (!photo.url_z) {
          photo.url_z = photo.url_m;
        }
        if (!photo.url_l) {
          photo.url_l = photo.url_z;
        }
        if (areaT > areaZ) {
          img.src = photo.url_l + '?' + _.constants.random;
        } else if (areaT > areaM) {
          img.src = photo.url_z + '?' + _.constants.random;
        } else if (areaT > areaS) {
          img.src = photo.url_m + '?' + _.constants.random;
        } else {
          img.src = photo.url_s + '?' + _.constants.random;
        }
        li = document.createElement('li');
        li.style.left = (i * _.elements.target.offsetWidth) + 'px';
        li.style.height = _.elements.target.offsetHeight + 'px';
        li.style.margin = '0';
        li.style.overflow = 'hidden';
        li.style.padding = '0';
        li.style.position = 'absolute';
        li.style.top = '0';
        li.style.width = _.elements.target.offsetWidth + 'px';
        li.appendChild(img);
        _.elements.images.appendChild(li);
        _.addEvent(img, 'load', _.onLoadImage);
      }
    };
    _.onLoadWindow = function(event) {
      _.elements.target = typeof _.elements.target === 'string' ? document.getElementById(_.elements.target) : _.elements.target;
      _.elements.target.innerHTML = '<div class="flickrshow-container" style="background:transparent;height:' + _.elements.target.offsetHeight + 'px;margin:0;overflow:hidden;padding:0;position:relative;width:' + _.elements.target.offsetWidth + 'px"><div class="flickrshow-loading" style="background:transparent url(' + _.constants.img_url + 'static/images/bg.png);border-radius:12px;height:24px;left:50%;margin:-12px 0 0 -120px;overflow:hidden;padding:0;position:absolute;top:50%;width:240px;-moz-border-radius:12px;-webkit-border-radius:12px"><div class="flickrshow-loading-bar" style="background:#000;border-radius:12px;height:24px;left:0;margin:0;padding:0;position:absolute;top:0;width:0;-moz-border-radius:12px;-webkit-border-radius:12px"></div></div><ul class="flickrshow-images" style="background:transparent;height:' + _.elements.target.offsetHeight + 'px;left:0;list-style:none;margin:0;padding:0;position:absolute;top:0;visibility:hidden;width:' + _.elements.target.offsetWidth + 'px"></ul><div class="flickrshow-buttons" style="background:transparent url(' + _.constants.img_url + 'static/images/bg.png);height:40px;margin:0;padding:0;position:absolute;top:' + _.elements.target.offsetHeight + 'px;width:' + _.elements.target.offsetWidth + 'px"><div class="flickrshow-buttons-left" style="background:#000 url(' + _.constants.img_url + 'static/images/il.png) 50% 50% no-repeat;border-radius:12px;cursor:pointer;height:24px;left:auto;margin:0;padding:0;position:absolute;right:40px;top:8px;width:24px;-moz-border-radius:12px;-webkit-border-radius:12px"></div><div class="flickrshow-buttons-right" style="background:#000 url(' + _.constants.img_url + 'static/images/ir.png) 50% 50% no-repeat;border-radius:12px;cursor:pointer;height:24px;left:auto;margin:0;padding:0;position:absolute;right:8px;top:8px;width:24px;-moz-border-radius:12px;-webkit-border-radius:12px"></div><div class="flickrshow-buttons-play" style="background:#000 url(' + _.constants.img_url + 'static/images/ip.png) 50% 50% no-repeat;border-radius:12px;cursor:pointer;height:24px;left:8px;margin:0;padding:0;position:absolute;right:auto;top:8px;width:24px;-moz-border-radius:12px;-webkit-border-radius:12px;"></div><p class="flickrshow-buttons-title" style="background:#000;border-radius:12px;color:#FFF;cursor:pointer;font:normal normal 600 11px/24px helvetica,arial,sans-serif;height:24px;left:40px;margin:0;overflow:hidden;padding:0;position:absolute;right:auto;text-align:center;text-shadow:none;text-transform:capitalize;top:8px;width:' + (_.elements.target.offsetWidth - 112) + 'px;-moz-border-radius:12px;-webkit-border-radius:12px">&nbsp</p></div></div>';
      _.elements.container = _.elements.target.childNodes[0];
      _.elements.buttons = _.elements.target.childNodes[0].childNodes[2];
      _.elements.images = _.elements.target.childNodes[0].childNodes[1];
      _.elements.loading = _.elements.target.childNodes[0].childNodes[0];
      if (false === _.settings.hide_buttons) {
        _.addEvent(_.elements.images, 'click', _.toggleButtons);
        _.addEvent(_.elements.container, 'mouseover', _.showButtons);
        _.addEvent(_.elements.container, 'mouseout', _.hideButtons);
        _.addEvent(_.elements.buttons.childNodes[0], 'click', _.onClickLeft);
        _.addEvent(_.elements.buttons.childNodes[1], 'click', _.onClickRight);
        _.addEvent(_.elements.buttons.childNodes[2], 'click', _.onClickPlay);
        _.addEvent(_.elements.buttons.childNodes[3], 'click', _.showFlickr);
      }
      window['flickrshow_jsonp_' + _.constants.random] = _.onLoadJson;
      _.elements.script = document.createElement('script');
      _.elements.script.async = true;
      _.elements.script.src = _.addUrl('flickrshow_jsonp_' + _.constants.random);
      (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(_.elements.script);
    };
    _.hideButtons = function() {
      if ((_.constants.isLoading === true) || (_.constants.isButtonsOpen === false)) {
        return;
      }
      _.constants.isButtonsOpen = false;
      _.animate(_.elements.buttons, 'top', _.elements.target.offsetHeight, _.constants.speed, 'buttons');
    };
    _.showButtons = function() {
      if ((_.constants.isLoading === true) || (_.constants.isButtonsOpen === true)) {
        return;
      }
      _.constants.isButtonsOpen = true;
      _.animate(_.elements.buttons, 'top', _.elements.target.offsetHeight - 40, _.constants.speed, 'buttons');
    };
    _.toggleButtons = function() {
      if (_.constants.isButtonsOpen === true) {
        _.hideButtons();
      } else {
        _.showButtons();
      }
    };
    _.showFlickr = function() {
      var img;
      img = _.elements.images.childNodes[_.constants.imageCurrent].childNodes[0];
      if (!(img != null)) {
        return;
      }
      window.location = 'http://www.flickr.com/photos/' + img.getAttribute('data-flickr-owner') + '/' + img.getAttribute('data-flickr-photo_id') + '/';
    };
    _.showTitle = function() {
      var img;
      img = _.elements.images.childNodes[_.constants.imageCurrent].childNodes[0];
      if (!(img != null)) {
        return;
      }
      _.elements.buttons.childNodes[3].innerHTML = (_.constants.imageCurrent + 1) + '/' + _.constants.imageTotal + ' - ' + img.getAttribute('data-flickr-title');
    };
    _.constants = {
      img_url: 'http://www.flickrshow.co.uk/',
      intervals: [],
      imageCurrent: 0,
      imageLoaded: 0,
      imageTotal: 0,
      isButtonsOpen: false,
      isLoading: true,
      isPlaying: false,
      random: Math.floor(Math.random() * 999999999999),
      speed: 100
    };
    _.elements = {
      buttons: null,
      button1: null,
      button2: null,
      button3: null,
      button4: null,
      container: null,
      images: null,
      loading: null,
      script: null,
      target: null
    };
    _.settings = {
      autoplay: false,
      gallery: null,
      group: null,
      hide_buttons: false,
      interval: 3000,
      license: '1,2,3,4,5,6,7',
      onLoad: null,
      onMove: null,
      onPlay: null,
      onPause: null,
      page: '1',
      person: null,
      per_page: '50',
      set: null,
      tags: null,
      user: null
    };
    _.elements.target = target;
    for (key in settings) {
      if (!__hasProp.call(settings, key)) continue;
      value = settings[key];
      _.settings[key] = value;
    }
    if (settings.flickr_group != null) {
      _.settings.group = settings.flickr_group;
    }
    if (settings.flickr_photoset != null) {
      _.settings.set = settings.flickr_photoset;
    }
    if (settings.flickr_tags != null) {
      _.settings.tags = settings.flickr_tags;
    }
    if (settings.flickr_user != null) {
      _.settings.user = settings.flickr_user;
    }
    _.addEvent(window, 'load', _.onLoadWindow);
    return {
      constants: _.constants,
      elements: _.elements,
      settings: _.settings,
      left: _.onClickLeft,
      right: _.onClickRight,
      play: _.onClickPlay
    };
  };
  if (window.jQuery != null) {
    window.jQuery.fn.flickrshow = function(settings) {
      return new flickrshow(window.jQuery(this)[0], settings);
    };
  }
}).call(this);
