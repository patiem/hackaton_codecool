(function() {
    var s = document.getElementById('wrap').style,
        f = false,
        c1 = 'steelblue',
        c2 = 'orangered',
        c3 = 'crimson';


    setInterval(function() {
        s.background = f ? c1 : c2;
        s.background = f ? c2 : c3;
        s.background = f ? c3 : c1;
        s.color = f ? c2 : c1;
        f = !f;
    }, 600);

    setInterval(function () {
        s.background = f ? c2 : c3;
    }, 600)
})();
