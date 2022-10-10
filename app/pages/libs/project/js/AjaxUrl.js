/**
 * ajax请求url
 */
var AjaxUrl = {
    project: {
        query: "/api/project/",
        add: "/api/project/",
        delete: "/api/project/[id]",
        update: "/api/project/"
    },
    vm: {
        query: "/api/vm/",
        query_multiple: "/api/vm/query_multiple/",
        add: "/api/vm/",
        delete: "/api/vm/[id]",
        update: "/api/vm/"
    },

    sys_role: {
        query: "/sys_mgmt/role/",
        add: "/sys_mgmt/role/",
        delete: "/sys_mgmt/role/[id]",
        update: "/sys_mgmt/role/"
    },
    sys_user: {
        query: "/sys_mgmt/user/query_multiple/",
        add: "/sys_mgmt/user/",
        delete: "/sys_mgmt/user/[id]",
        update: "/sys_mgmt/user/"
    },
    sys_op_log: {
        query: {url: "/sys_mgmt/op_log/query_pss/", method: "POST"},
        menu: "/sys_mgmt/op_log/menu/"
    },
    sys_auth: {
        login: {url: "/sys_mgmt/auth/login/", method: "POST"},
        // login: {url: "/sys_mgmt/auth/token/", method: "POST"},
        logout: {url: "/sys_mgmt/auth/logout/", method: "GET"},

        query: "/sys_mgmt/auth/account/",
        update: "/sys_mgmt/auth/account/"
    }
};
