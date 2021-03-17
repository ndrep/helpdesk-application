import "@babel/polyfill";
import "mutationobserver-shim";
import Vue from "vue";
import "./plugins/bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import store from "./store";
import "vuetify/dist/vuetify.min.css";
import Vuetify from "vuetify";
import ElementUI from "element-ui";
import locale from "element-ui/lib/locale/lang/it";

Vue.use(Vuetify);
Vue.use(ElementUI, { locale });
Vue.config.devtools = true;

const ignoreWarnMessage =
  "The .native modifier for v-on is only valid on components but it was used on <div>.";
Vue.config.warnHandler = function(msg, vm, trace) {
  trace;
  if (msg === ignoreWarnMessage) {
    msg = null;
    vm = null;
    trace = null;
  }
};

new Vue({
  router,
  vuetify,
  store,
  render: h => h(App)
}).$mount("#app");
