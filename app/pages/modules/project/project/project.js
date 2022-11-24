var Project = z.util.mergeObject(pro.template.CRUDTablePage, {
    page_options: {
        url: AjaxUrl.project,
        grid_options: {
            columns: [
                {name: "名称", field: "name", width: 100},
                {name: "仓库", field: "repository"},
                {name: "分支", field: "branch", width: 80},
                {name: "token", field: "token", "minimizable": true, "minimized": true},
                {name: "username", field: "username", "minimizable": true, width: 160},
                {name: "password", field: "password", "minimizable": true, width: 120},
                {
                    name: "虚拟机", field: "vms", minimizable: true, width: 150,
                    render: function (td, data) {
                        var vms = data.get("vms") || [];
                        var infos = [];
                        vms.forEach(function (vm) {
                            var status;
                            if (vm.status === true) {
                                status = "<i class='fa fa-check-circle color-success'></i>";
                            } else {
                                status = "<i class='fa fa-exclamation-triangle color-warning'></i>";
                            }
                            var info = vm.host + "&nbsp;&nbsp;&nbsp;" + status;
                            infos.push(info);
                        });
                        pro.GridUtil.createNestedGrid(td, infos);
                    }
                },
                {
                    name: "上次触发时间", field: "last_trig", width: 150,
                    render: function (td, data) {
                        td.innerHTML = pro.TimeUtil.format(data.get("last_trig"));
                    }
                },
                {
                    name: "操作", width: 180, fixed: "right",
                    render: function (td, data, column) {
                        pro.GridUtil.createOPButton(td, data, "enable", "<i class='text-danger fa fa-play' title='运行'></i>运行",
                            function () {
                                Project.deployProject(data);
                            }, {
                                className: 'btn btn-link color-success'
                            })
                        pro.template.CRUDTablePage.renderUpdateColumn(td, data, column);
                    }
                }
            ]
        }
    }
}, {
    init: function () {
        var _this = this;
        this.vmGrid = z.widget.Grid({
            appendTo: "#vmsGridDiv",
            overflow: false,
            sortable: false,
            columns: [
                {name: "hostname", field: "host", width: 100},
                {name: "username", field: "username", "minimizable": true, width: 85},
                {name: "password", field: "password", "minimizable": true, width: 85},
                {name: "本地仓库目录", field: "git_dir", "minimizable": true},
                {name: "重部署命令", field: "deploy_command", "minimizable": true, "minimized": true},
                {name: "检查命令", field: "check_command", "minimizable": true},
                {
                    name: "操作", width: 120, fixed: "right",
                    render: function (td, data, column) {
                        pro.GridUtil.renderUpdateDeleteOperateButton(null, data, "edit", td, function () {
                            _this.showNestedModal("#vmModalDiv");
                            _this._current_edit_vm = data;
                            _this.vmForm.setValue(data.gets());
                        }, function (event) {
                            _this.vmGrid.removeData(data);
                        });
                    }
                }
            ]
        });
        this.vmForm = new z.form.Form("#vmModalDiv");

        z.dom.event.onclick("#addVMBtn", function () {
            this.vmForm.clearValue();
            this._current_edit_vm = null;
            this.showNestedModal("#vmModalDiv")
        }, this);

        z.dom.event.onclick("#vmModalOkBtn", function () {
            var value = this.vmForm.getValue();
            if (value == null) {
                return;
            }
            if (this._current_edit_vm) {
                this._current_edit_vm.set(value);
            } else {
                this.addVMGridData(value);
            }
            z.widget.modal("#vmModalDiv", false);
        }, this);
    },
    getFormValue: function () {
        var value = this.form.getValue();
        if (value) {
            var vms = [];
            this.vmGrid.getDataArray().forEach(function (vm) {
                vms.push(vm.gets());
            });
            value.vms = vms;
        }
        return value;
    },
    onShowFormModal: function (editType, initValue) {
        this.setVMGridData(initValue.vms);
    },
    setVMGridData: function (vms) {
        this.vmGrid.setData(vms || []);
        this.vmGrid.update();
    },
    addVMGridData: function (vmInfo) {
        this.vmGrid.addData(vmInfo);
    },
    deployProject: function (data) {
        pro.AjaxCRUD.ajax({
            url: AjaxUrl.project.deploy,
            method: 'POST',
            data: data.gets(),
            success_notify: true,
            complete: function (result) {
                data.set("vms", result.data.vms);
            }
        });
    }
});