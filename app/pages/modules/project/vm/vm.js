var VM = z.util.mergeObject(pro.template.CRUDTablePage, {
    page_options: {
        url: z.util.mergeObject({}, AjaxUrl.vm, {query: AjaxUrl.vm.query_multiple}),
        grid_options: {
            columns: [
                {name: "主机", field: "host", width: 120},
                {name: "username", field: "username", width: 100},
                {name: "password", field: "password", width: 100},
                {name: "本地仓库目录", field: "git_dir", "minimizable": true, width: 300},
                {name: "重部署命令", field: "deploy_command", "minimizable": true, "minimized": true},
                {name: "检查命令", field: "check_command", "minimizable": true, width: 200},
                {
                    name: "部署结果", field: "status", width: 100, render: function (td, data) {
                        z.dom.setStyle(td, "text-align", "center");
                        if (data.get("status") === true) {
                            td.innerHTML = "<i class='fa fa-check-circle color-success'></i>";
                        } else {
                            td.innerHTML = "<i class='fa fa-exclamation-triangle color-warning'></i>";
                        }
                    }
                },
                {
                    name: "上次触发时间", field: "last_trig",
                    render: function (td, data) {
                        td.innerHTML = pro.TimeUtil.format(data.get("last_trig"));
                    }
                },
                {
                    name: "操作", width: 150, fixed: "right",
                    render: function (td, data, column) {
                        pro.template.CRUDTablePage.renderUpdateColumn(td, data, column);
                    }
                },
                {
                    name: "updated_at", field: "updated_at", "minimizable": true, "minimized": true,
                    render: function (td, data) {
                        td.innerHTML = pro.TimeUtil.format(data.get("updated_at"));
                    }
                },
                {
                    name: "created_at", field: "created_at", "minimizable": true, "minimized": true,
                    render: function (td, data) {
                        td.innerHTML = pro.TimeUtil.format(data.get("updated_at"));
                    }
                }
            ]
        }
    }
}, {
    setGridData: function (result, data) {
        // this.projects = data.projects || [];
        z.dom.initSelectOptions("[ze-model=project_id]", data.projects);
        this.grid.setData(data.vms);
    }
});