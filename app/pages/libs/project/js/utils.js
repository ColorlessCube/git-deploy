/*
* 常用方法
* */
var Utils = {
    vendorMapping: {
        cisco: "Cisco",
        huawei: "华为",
        zhongxing: "中兴",
        juniper: "Juniper"
    },
    analyzeLabelMapping: {
        normal: "正常",
        abnormal: "异常"
    },
    getCurrentTime: function () {
        return z.util.formatDate(new Date());
    },
    getNowStartAndEndTime: function (range, delay, unit) {
        var end_time = new Date();
        var start_time = new Date();
        if (unit === 'day') {
            end_time.setDate(end_time.getDate() - delay);
            start_time.setDate(end_time.getDate() - range - delay);
        } else if (unit === 'hour') {
            end_time.setHours(end_time.getHours() - delay);
            start_time.setHours(end_time.getHours() - range - delay);
        } else if (unit === 'minute') {
            end_time.setMinutes(end_time.getMinutes() - delay);
            start_time.setMinutes(end_time.getMinutes() - range - delay);
        } else if (unit === 'second') {
            end_time.setSeconds(end_time.getSeconds() - delay);
            start_time.setSeconds(end_time.getSeconds() - range - delay);
        }
        start_time = z.util.formatDate(start_time);
        end_time = z.util.formatDate(end_time);
        return {
            start_time: start_time,
            end_time: end_time
        }
    },
    deleteObjectFirstProperty: function (obj) {
        for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
                delete obj[key];
                break;
            }
        }
    }
}
