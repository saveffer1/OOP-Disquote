//DataTables
//Sort file size data.
jQuery.extend(jQuery.fn.dataTableExt.oSort, {
    "file-size-units": {
        K: 1024,
        M: Math.pow(1024, 2),
        G: Math.pow(1024, 3),
        T: Math.pow(1024, 4),
        P: Math.pow(1024, 5),
        E: Math.pow(1024, 6)
    },

    "file-size-pre": function (a) {
        var x = a.substring(0, a.length - 1);
        var x_unit = a.substring(a.length - 1, a.length);
        if (jQuery.fn.dataTableExt.oSort['file-size-units'][x_unit]) {
            return parseInt(x * jQuery.fn.dataTableExt.oSort['file-size-units'][x_unit], 10);
        }
        else {
            return parseInt(x + x_unit, 10);
        }
    },

    "file-size-asc": function (a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "file-size-desc": function (a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});

//DataTables
//Sort numeric data which has a percent sign with it.
jQuery.extend(jQuery.fn.dataTableExt.oSort, {
    "percent-pre": function (a) {
        var x = (a === "-") ? 0 : a.replace(/%/, "");
        return parseFloat(x);
    },

    "percent-asc": function (a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "percent-desc": function (a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});

//DataTables
//Sort IP addresses
jQuery.extend(jQuery.fn.dataTableExt.oSort, {
    "ip-address-pre": function (a) {
        // split the address into octets
        //
        var x = a.split('.');

        // pad each of the octets to three digits in length
        //
        function zeroPad(num, places) {
            var zero = places - num.toString().length + 1;
            return new Array(+(zero > 0 && zero)).join("0") + num;
        }

        // build the resulting IP
        var r = '';
        for (var i = 0; i < x.length; i++)
            r = r + zeroPad(x[i], 3);

        // return the formatted IP address
        //
        return r;
    },

    "ip-address-asc": function (a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "ip-address-desc": function (a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});

// If dataTable with provided ID exists, destroy it.
function destroy_dataTable(table_id) {
    var table = $("#" + table_id);
    var ex = document.getElementById(table_id);
    if ($.fn.DataTable.fnIsDataTable(ex)) {
        table.hide().dataTable().fnClearTable();
        table.dataTable().fnDestroy();
    }
}

getJSON = async function () {
    return fetch(`/admin/info`, {
        method: 'GET',
        credentials: 'include'
    })
        .then((response) => response.json())
        .then((responseJson) => { return responseJson });
}

function destroy_dataTable(table_id) {
    var table = $("#" + table_id);
    var ex = document.getElementById(table_id);
    if ($.fn.DataTable.fnIsDataTable(ex)) {
        table.hide().dataTable().fnClearTable();
        table.dataTable().fnDestroy();
    }
}

info = async function () {
    const json = await this.getJSON().then(async (data) => {
        $("#get-osname").text(data.platform);
        $("#get-uptime").text(data.uptime);
        $("#get-hostname").text(data.ipaddress);
        $("#get-cpucount").text(data.cores.cpus);
        $("#get-cputype").text(data.cores.type);
        $("#cpuf").text(data.cpu.free);
        $("#cpuu").text(data.cpu.used);
        $("#memf").text(data.memory.free);
        $("#memu").text(data.memory.usage);
        // $("#memp").text(data.memory.percent);
        // create table with get_proc id with data.cpu.all
        var table = $("#get_proc");
        table.dataTable({
            "bProcessing": true,
            "aaData": data.cpu.all,
            "aoColumns": [
                { "sTitle": "PID", "mData": "pid" },
                { "sTitle": "Name", "mData": "name" },
                { "sTitle": "CPU", "mData": "cpu_percent" }
            ],
            "bDestroy": true,
            "bPaginate": false,
            "bFilter": false,
            "bInfo": true,
            "bSort": true
        });
    });
}

// Expand-Contract div/table
$(document).ready(function () {
    $(".widget-content").show();
    $(".widget-header").click(function () {
        $(this).next(".widget-content").slideToggle(500);
        $("i", this).toggleClass("icon-minus icon-plus");
    });
});
