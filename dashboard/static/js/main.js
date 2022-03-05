var app1 = Vue.createApp({})
app1.component('app-component1', {
    template: `
        <div>
            <h1> APP 1 </h1>
        </div>
    `
})
app1.mount("#app1")


var app2 = Vue.createApp({})
app2.component('app-component2', {
    template: `
        <div>
            <h1> APP 2 </h1>
        </div>
    `
})
app2.mount("#app2")


var app = Vue.createApp({
    data: () => {
        return {
            showcomp1: true,
            showcomp2: false
        }
        
    },
    methods: {
        switchiii(){
            this.showcomp1 = !this.showcomp1
            this.showcomp2 = !this.showcomp1
        }
    }
})
app.mount('#app')