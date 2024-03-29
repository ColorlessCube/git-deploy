//中文文字
z.setDefault({
    WIDGET_MESSAGEBOX_CONFIRM_TEXT: "确认",
    WIDGET_MESSAGEBOX_CANCEL_TEXT: "取消",

    PRO_GRID_OPERATE_UPDATE_LABEL: "编辑",
    PRO_GRID_OPERATE_DELETE_LABEL: "删除",

    PRO_GRID_RESULT_SUCCESS_LABEL: "成功",
    PRO_GRID_RESULT_FAIL_LABEL: "失败",

    PRO_AJAX_QUERY_TIPS: "查询",
    PRO_AJAX_ADD_TIPS: "添加",
    PRO_AJAX_CREATE_TIPS: "创建",
    PRO_AJAX_READ_TIPS: "读取",
    PRO_AJAX_UPDATE_TIPS: "编辑",
    PRO_AJAX_DELETE_TIPS: "删除",

    PRO_AJAX_UPLOAD_TIPS: "上传",

    PRO_AJAX_TIMEOUT_TIPS: "超时",
    PRO_AJAX_FORBIDDEN_TIPS: "禁止访问",
    PRO_AJAX_EXCEPTION_TIPS: "请求异常",
    PRO_AJAX_CLIENT_ERROR_TIPS: "请求错误",
    PRO_AJAX_SERVER_ERROR_TIPS: "服务器错误",
    PRO_AJAX_SUCCESS_TIPS: "成功",
    PRO_AJAX_FAIL_TIPS: "失败",

    PRO_MESSAGE_TIPS: "提示",
    PRO_MESSAGE_DELETE_CONFIRM: "确认删除?",

    PRO_MODAL_UPDATE_TITLE: "编辑",
    PRO_MODAL_ADD_TITLE: "添加",
    PRO_MODAL_VIEW_TITLE: "查看",

    PRO_MODAL_CONFIRM_TEXT: "确认",
    PRO_MODAL_CANCEL_TEXT: "取消"
});

z.form.Validator.registerRuleMessage({
    required: '请输入',
    integer: '请输入整数',
    numeric: '请输入数字',
    alphanumeric: '请输入字母/数字',
    alphanumeric_dash: '请输入字母/数字/中划线/下划线',
    alphanumeric_space: '请输入字母/数字/空格',
    email: '请输入Email',
    ipv4: '请输入IP地址',
    minlength: '该字段至少包含%p个字符',
    maxlength: '该字段不得超过%p个字符',
    greaterthan: '请输入大于%p的数字',
    lessthan: '请输入小于%p的数字',
    equal: '该字段必须和%p一致',
    match: '该字段必须和%p字段一致'
});

//图标
z.setDefault({
    PRO_GRID_OPERATE_UPDATE_LABEL: "<i class='fa fa-edit'></i>编辑",
    PRO_GRID_OPERATE_DELETE_LABEL: "<i class='fa fa-trash-o'></i>删除",
    PRO_MESSAGE_DELETE_CONFIRM: "<i class='fa fa-warning color-warning'></i> 确认删除?",
    PRO_MODAL_UPDATE_TITLE: "<i class='fa fa-edit'></i> 编辑",
    PRO_MODAL_ADD_TITLE: "<i class='fa fa-plus-square'></i> 添加",
    PRO_MODAL_VIEW_TITLE: "<i class='fa fa-file-text-o'></i> 查看"
});

//项目定制化
z.setDefault({
    FORM_VALIDATE_ERROR_CLASS: "is-invalid",
    FORM_VALIDATE_MESSAGE_CLASS: "invalid-feedback",

    PRO_GRID_OPERATE_UPDATE_CLASS: "btn btn-link color-primary",
    PRO_GRID_OPERATE_DELETE_CLASS: "btn btn-link color-danger",

    // PRO_AJAX_NOTIFY_OPTIONS: {position: "bottom_right"},

    PRO_CRUDTABLEPAGE_MODAL_OPTIONS: {open_animation: "z-animation-fadeInLeft", close_animation: "z-animation-fadeOutRight"},
    PRO_CRUDTABLEPAGE_NESTED_MODAL_OPTIONS: {open_animation: "z-animation-fadeInUp", close_animation: "z-animation-fadeOutDown"}
});


/**
 * ajax请求url
 */
var AjaxUrl = {
    sys_role: {
        query: "/sys-mgmt/roles/",
        add: "/sys-mgmt/roles/",
        delete: "/sys-mgmt/roles/[id]",
        update: "/sys-mgmt/roles/"
    },
    sys_user: {
        query: "/sys-mgmt/users/multi/",
        add: "/sys-mgmt/users/",
        delete: "/sys-mgmt/users/[id]",
        update: "/sys-mgmt/users/"
    },
    sys_license: {
        query: "/sys-mgmt/licenses/",
        add: {url: "/sys-mgmt/licenses/", method: "POST"}
    },
    sys_action_log: {
        query: {url: "/sys-mgmt/action-logs/pss/", method: "POST"},
        modules: "/sys-mgmt/modules/"
    },
    sys_auth: {
        login: {url: "/sys-mgmt/auth/login/", method: "POST"},
        // login: {url: "/sys-mgmt/auth/token/", method: "POST"},
        logout: {url: "/sys-mgmt/auth/logout/", method: "GET"},

        query: "/sys-mgmt/auth/account/",
        update: "/sys-mgmt/auth/account/"
    },

    project: {
        query: "/api/v1.0/project/",
        add: "/api/v1.0/project/",
        delete: "/api/v1.0/project/[id]",
        update: "/api/v1.0/project/",
        deploy: "/api/v1.0/deploy/manual"
    },
    vm: {
        query: "/api/v1.0/vm/",
        query_multiple: "/api/v1.0/vm/query_multiple/",
        add: "/api/v1.0/vm/",
        delete: "/api/v1.0/vm/[id]/",
        update: "/api/v1.0/vm/"
    },
};


/**
 * ajax数据缓存
 */
var AjaxCache = {
    action_logs_modules: {
        _key: "flasky_ajax_cache_action_logs_modules",
        query: function (callback, context) {
            var key = AjaxCache.action_logs_modules._key;
            var data = z.bom.getLocalStorage(key);
            if (data) {
                callback.apply(context, [data]);
                return;
            }
            pro.AjaxCRUD.query({
                url: AjaxUrl.sys_action_log.modules,
                success_notify: false,
                success: function (result) {
                    var menus = result.data;
                    menus.forEach(function (item) {
                        if (item.module) {
                            item.value = item.module;
                        }
                    });
                    var levelMenus = pro.DataUtil.parseLevelData(menus);
                    menus.forEach(function (item) {
                        delete item.id;
                        delete item.parent_id;
                    });
                    callback.apply(context, [levelMenus]);
                    z.bom.setLocalStorage(key, levelMenus, 2880);
                }
            });
        }
    },
    clear: function () {
        z.bom.clearSessionStorage();
    }
};

var refreshMenuByPath = function (paths) {
    var admin = window.top.Admin;
    if (admin) {
        admin.refreshMenu(paths)
    }
};
z.setDefault({
    "AJAX_BEFORE_SEND": function (httpRequest) {
        httpRequest.setRequestHeader("Authorization", z.bom.getLocalStorage("auth-token"));
    },
    "AJAX_COMPLETE": function (httpRequest) {
        var status = httpRequest.status;
        if (status === 200) {
            var responseType = httpRequest.responseType;
            if (responseType === "" || responseType === "text") {
                try {
                    var result = JSON.parse(httpRequest.responseText);
                    if (result.status !== z.getDefault("PRO_AJAX_SUCCESS_STATE") && result.status_code === 'uri_unauthorized') {
                        var pathname = window.location.pathname;
                        if (pathname === "/" || pathname === "/index" || pathname === "index") {
                            window.top.location.href = "/login";
                        } else {
                            z.widget.alert("请先登录!!", "提示", function (result) {//callback
                                window.top.location.href = "/login";
                            });
                        }
                    }
                } catch (err) {
                }
            }
        }
    }
});
/*
if (pro) {
    var _createGrid = pro.template.CRUDTablePage._createGrid;
    pro.template.CRUDTablePage._createGrid = function () {
        var grid = _createGrid.apply(pro.template.CRUDTablePage, arguments);
        var pagination = this.gridPagination;
        if (pagination) {
            pagination.set("total_template", "<%start%>-<%end%> | <%total%>  跳转至<input id='jumpInput' class='sizes' style='width:2.6em'>页");
            var _updateTotalInfo = pagination._updateTotalInfo
            pagination._updateTotalInfo = function () {
                _updateTotalInfo.apply(pagination, arguments);
                var jumpInput = z.dom.query("#jumpInput", pagination.getRoot());
                if (jumpInput && jumpInput._inited !== true) {
                    jumpInput._inited = true;
                    z.dom.event.onchange(jumpInput, function () {
                        var pageConfig = pagination.getPageConfig();
                        var index = Math.min(Math.max(1, jumpInput.value | 0), pageConfig.number);
                        pagination.set("page_index", index);
                        jumpInput.value = "";
                    });
                }
            }
        }
        return grid;
    }
}
*/


/*
z.ajax.setup({
    beforeSend: function (httpRequest) {
        httpRequest.setRequestHeader("Authorization", z.bom.getLocalStorage("auth-token"));
    },
    complete: function (httpRequest) {
        var status = httpRequest.status;
        if (status === 200) {
            var responseType = httpRequest.responseType;
            if (responseType === "" || responseType === "text") {
                var result = JSON.parse(httpRequest.responseText);
                if (result.status !== z.getDefault("PRO_AJAX_SUCCESS_STATE") && result.status_code === 'uri_unauthorized') {
                    var pathname = window.location.pathname;
                    if (pathname === "/" || pathname === "/index" || pathname === "index") {
                        window.top.location.href = "/login";
                    } else {
                        z.widget.alert("请先登录!!", "提示", function (result) {//callback
                            window.top.location.href = "/login";
                        });
                    }
                }
            }
        }
    }
});*/


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




