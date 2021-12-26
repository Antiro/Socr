new Vue({
    el: '#topic',
    data() {
        return {
            dr:"#35363A",
            lg:"#FFFFFF",
            Vis: false,
            Scr: true,
        };
    },

    methods: {
        dark() {
            document.body.style.backgroundColor = this.dr;

            this.Vis = !this.Vis;
            this.Scr = !this.Scr;
        },

        light() {
            document.body.style.backgroundColor = this.lg;

            this.Vis = !this.Vis;
            this.Scr = !this.Scr;
        },
    },
});