var remain = 10;
var startTime = new Date().getTime();
$(document).ready(function() {
    setTimeout(timeoutHandler, 1000);
    setTimeout(doChallange, 1000)
});
function timeoutHandler() {
    remain = remain - 1;
    $("#remain").text(remain);
    if (remain > 0) {
        setTimeout(timeoutHandler, 1000)
    } else {
        doSubmit(randomString(100))
    }
}
function doChallange() {
    var aywcUid = genOrGetAywcUid();
    var genApi = "/anti/recaptcha/v4/gen?aywcUid=" + aywcUid + "&_=" + new Date().getTime();
    $.get(genApi, function(genResult) {
        var costtime = new Date().getTime() - startTime;
        if (genResult.errno == 0) {
            var recaptchaForm = $("#recaptcha-form");
            if (recaptchaForm.length > 0) {
                var tokenInput = $("<input type='hidden' name='token'/>");
                tokenInput.attr("value", genResult.token);
                recaptchaForm.append(tokenInput);
                var aywcUid = genOrGetAywcUid();
                var unifyidInput = $("<input type='hidden' name='aywcUid'/>");
                unifyidInput.attr("value", aywcUid);
                recaptchaForm.append(unifyidInput);
                var costtimeInput = $("<input type='hidden' name='costtime'/>");
                costtimeInput.attr("value", costtime);
                recaptchaForm.append(costtimeInput);
                recaptchaForm.submit()
            }
        } else {
            setTimeout(doChallange, 1000)
        }
    }, "json").fail(function(date, status) {
        console.log(new Date() + ": " + status);
        setTimeout(doChallange, 1000)
    })
}
function doSubmit(token) {
    var costtime = new Date().getTime() - startTime;
    var recaptchaForm = $("#recaptcha-form");
    if (recaptchaForm.length > 0) {
        var tokenInput = $("<input type='hidden' name='token'/>");
        tokenInput.attr("value", token);
        recaptchaForm.append(tokenInput);
        var aywcUid = genOrGetAywcUid();
        var unifyidInput = $("<input type='hidden' name='aywcUid'/>");
        unifyidInput.attr("value", aywcUid);
        recaptchaForm.append(unifyidInput);
        var costtimeInput = $("<input type='hidden' name='costtime'/>");
        costtimeInput.attr("value", costtime);
        recaptchaForm.append(costtimeInput);
        recaptchaForm.submit()
    }
}
function genOrGetAywcUid() {
    var rootDomain = parseRootDomain(); // .skrbtju.top
    var unifyidKey = "aywcUid";
    var aywcUid = $.cookie(unifyidKey);
    if (isEmpty(aywcUid)) {
        aywcUid = randomString(10) + "_" + formatDate("yyyyMMddhhmmss", new Date());
        $.cookie(unifyidKey, aywcUid, {
            domain: rootDomain,
            path: "/",
            expires: 3650
        })
    }
    return aywcUid
}
function isEmpty(x) {
    if (x == null || x == undefined || x == "") {
        return true
    } else {
        return false
    }
}
function randomString(len, charSet) {
    charSet = charSet || "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var randomString = "";
    for (var i = 0; i < len; i++) {
        var randomPoz = Math.floor(Math.random() * charSet.length);
        randomString += charSet.substring(randomPoz, randomPoz + 1)
    }
    return randomString
}
function formatDate(fmt, date) {
    var o = {
        "M+": date.getMonth() + 1,
        "d+": date.getDate(),
        "h+": date.getHours(),
        "m+": date.getMinutes(),
        "s+": date.getSeconds(),
        "q+": Math.floor((date.getMonth() + 3) / 3),
        "S": date.getMilliseconds()
    };
    if (/(y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length))
    }
    for (var k in o) {
        if (new RegExp("(" + k + ")").test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)))
        }
    }
    return fmt
}
function parseRootDomain() {
    var rootDomain = location.host;
    tokens = rootDomain.split(".");
    if (tokens.length != 1) {
        rootDomain = "." + tokens[tokens.length - 2] + "." + tokens[tokens.length - 1]
    }
    return rootDomain
}
;