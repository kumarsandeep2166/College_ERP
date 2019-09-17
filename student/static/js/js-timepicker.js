(function (root) {

    "use strict";

    /**
     * Common object params
     * @type {Object}
     */
    var common = {
            publicMethods: ['show', 'hide', 'getTime', 'setTime', 'destroy'],
            className: 'JsTimepicker'
        },
        /**
         * Main constructor
         * @return {Object} - this handle
         */
        Protected = function (handle, options) {

            var n;

            this.name = 'js-timepicker' + Math.floor(Math.random() * 99999);

            this.settings = {
                hourLeadingZero: true,
                hourStep: 1,
                minuteLeadingZero: true,
                minuteStep: 5
            };

            //apply options to settings 
            if (options) {
                for (n in options) {
                    if (options.hasOwnProperty(n)) {
                        this.settings[n] = options[n];
                    }
                }
            }

            this.handle = handle;

            this.isVisible = false;
            this.hourArray = this.getHoursArray(this.settings.hourStep, this.settings.hourLeadingZero);
            this.minuteArray = this.getMinutesArray(this.settings.minuteStep, this.settings.minuteLeadingZero);
            this.timepicker = this.makeTimepickerHtml();
            this.setEvents();
            
            return this;
        };



    /**
     * Main prototype
     * @type {Object}
     */
    Protected.prototype = {

        event_outClick: function (e) {
            var self = this,
                parentElem = e.target,
                closeList = true;

            if (this.isVisible && (parentElem !== self.timepicker) && (parentElem !== this.handle)) {

                while (parentElem && parentElem.parentNode) {

                    if (parentElem === self.timepicker) {
                        closeList = false;
                        break;
                    }

                    parentElem = parentElem.parentNode;
                }
                closeList && self.hide();
            }
        },
        event_clickOnPicker: function (e) {

            if (e.target && e.target.getAttribute('data-hour')) {
                this.timepicker.querySelector('[data-hour].active') && this.timepicker.querySelector('[data-hour].active').classList.remove('active');
                e.target.classList.add('active');
                this.setHour(e.target.getAttribute('data-hour'));
                return;
            }

            if (e.target && e.target.getAttribute('data-minute')) {
                this.timepicker.querySelector('[data-minute].active') && this.timepicker.querySelector('[data-minute].active').classList.remove('active');
                e.target.classList.add('active');
                this.setMinute(e.target.getAttribute('data-minute'));
                return;
            }
        },
        setEvents: function () {
            var self = this;
            self.show = this.show.bind(this);
            self.event_outClick = this.event_outClick.bind(this);
            self.event_clickOnPicker = this.event_clickOnPicker.bind(this);
            
            Array.prototype.forEach.call(['click'], function (evt) {
                self.handle.addEventListener(evt, self.show);
            });

            document.addEventListener('click', self.event_outClick);
            this.timepicker.addEventListener('click', self.event_clickOnPicker);
        },
        unsetEvents: function () {
            var self = this;
            Array.prototype.forEach.call(['click'], function (evt) {
                self.handle.removeEventListener(evt, self.show);
            });
            document.removeEventListener('click', self.event_outClick);
            this.timepicker.removeEventListener('click', self.event_clickOnPicker);
        },
        getHoursArray: function (step) {
            var i, h = 24, retData = [];

            step = step || 1;

            for (i = 0; i < h; i += step) {
                retData.push(this.leadingZeroHour(i));
            }

            return retData;
        },
        getMinutesArray: function (step) {
            var i, h = 60, retData = [];

            step = step || 5;

            for (i = 0; i < h; i += step) {
                retData.push(this.leadingZeroMinute(i));
            }

            return retData; 
        },
        getPosition: function (element) {
            var xPosition = 0,
                yPosition = 0;
          
            while(element) {
                xPosition += (element.offsetLeft - element.scrollLeft + element.clientLeft);
                yPosition += (element.offsetTop - element.scrollTop + element.clientTop);
                element = element.offsetParent;
            }

            return {
                x: xPosition,
                y: yPosition
            };
        },
        getElementTime: function (asString) {
            var timeObj = this.parseTime(this.handle.value);
            return (asString ? timeObj.hour + ':' + timeObj.minute : timeObj);
        },
        parseTime: function (timeString) {
            var timeObj = {
                hour: timeString.split(':')[0] || '',
                minute: timeString.split(':')[1] || ''
            }

            timeObj.hour = this.leadingZeroHour(timeObj.hour);
            timeObj.minute = this.leadingZeroMinute(timeObj.minute);
            return timeObj;
        },
        setHour: function (hour) {
            this.handle.value = this.leadingZeroHour(hour) + ':' + this.getElementTime().minute;
        },
        setMinute: function (minute) {
            this.handle.value = this.getElementTime().hour + ':' + this.leadingZeroMinute(minute);
        },
        leadingZeroMinute: function (num) {
            return ((num === '') ? '' : (this.settings.minuteLeadingZero ? ('0' + num.toString()).substr(-2) : num.toString()));
        },
        leadingZeroHour: function (num) {
            return ((num === '') ? '' : (this.settings.hourLeadingZero ? ('0' + num.toString()).substr(-2) : num.toString()));
        },
        validateTime: function (timeString) {
            return new RegExp(/^\d{1,2}:\d{1,2}$/).test(timeString);
        },
        makeTimepickerHtml: function () {

            var container = document.createElement('div'),
                hourContainer = document.createElement('div'),
                minuteContainer = document.createElement('div'),
                elem;

            container.setAttribute('class', 'js-t');
            container.setAttribute('id', this.name + '-' + this.handle.name);
            hourContainer.setAttribute('class', 'js-t-hour-container');
            minuteContainer.setAttribute('class', 'js-t-minute-container');

            Array.prototype.forEach.call(this.hourArray, function (hour) {
                elem = document.createElement('div');
                elem.setAttribute('class', 'js-t-hour');
                elem.setAttribute('data-hour', hour.toString());
                elem.innerHTML = hour;
                hourContainer.appendChild(elem);
            });

            Array.prototype.forEach.call(this.minuteArray, function (minute) {
                elem = document.createElement('div');
                elem.setAttribute('class', 'js-t-minute');
                elem.setAttribute('data-minute', minute.toString());
                elem.innerHTML = minute;
                minuteContainer.appendChild(elem);
            });

            container.appendChild(hourContainer);
            container.appendChild(minuteContainer);

            return container;
            
        },
        show: function () {

            if (this.isVisible) {
                return false;
            }

            document.body.appendChild(this.timepicker);
            
            Array.prototype.forEach.call(this.timepicker.querySelectorAll('.active'), function (activeElem) {
                activeElem.classList.remove('active');
            });

            var handlePos = this.getPosition(this.handle),
                timeObj = this.getElementTime(),
                activeHour = this.timepicker.querySelector('[data-hour="' + timeObj.hour + '"]'),
                activeMinute = this.timepicker.querySelector('[data-minute="' + timeObj.minute + '"]');

            activeHour && activeHour.classList.add('active');
            activeMinute && activeMinute.classList.add('active');
            this.timepicker.style.left = handlePos.x.toString() + 'px';
            this.timepicker.style.top = (handlePos.y + this.handle.offsetHeight).toString() + 'px';
            this.timepicker.classList.add('visible');
            this.isVisible = true;

            return true;
        },
        hide: function () {
 
            if (!this.isVisible) {
                return false;
            }

            !this.validateTime(this.getElementTime(true)) && (this.handle.value = '');
            this.timepicker.classList.remove('visible');
            this.timepicker.style.top = '';
            this.isVisible = false;
            this.timepicker.remove();
            return true;
        },
        destroy: function () {
            this.hide();
            this.unsetEvents();
        },
        getTime: function () {
            return this.getElementTime(true);
        },
        setTime: function (hourOrTimeString, minute) {
            var timeObj = !minute ? this.parseTime(hourOrTimeString) : this.parseTime(hourOrTimeString.toString() + ':' + minute.toString());
            
            // check to step value
            if ((timeObj.minute % this.settings.minuteStep)) {
                console.error('Invalid time. Number does not match the minute step');
                return;
            }
            if ((timeObj.hour % this.settings.hourStep)) {
                console.error('Invalid time. Number does not match the hour step');
                return;
            }

            this.setHour(timeObj.hour);
            this.setMinute(timeObj.minute);
            this.handle.value = timeObj.hour + ':' + timeObj.minute;

            this.isVisible && this.hide() && this.show();
        }

    };
    

    root[common.className] = function () {

        function construct(constructor, args) {

            function Class() {
                return constructor.apply(this, args);
            }
            Class.prototype = constructor.prototype;
            return new Class();
        }

        var original = construct(Protected, arguments),
            Publicly = function () {};
        
        Publicly.prototype = {};
        Array.prototype.forEach.call(common.publicMethods, function (member) {
            Publicly.prototype[member] = function () {
                return original[member].apply(original, arguments);
            };
        });

        return new Publicly(arguments);
    };

}(this));