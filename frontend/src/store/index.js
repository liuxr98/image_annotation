import Vue from "vue"
import Vuex from "vuex"
import labelGroup from "@/store/modules/labelGroup";
import dataset from "@/store/modules/dataset";
import annotate from "@/store/modules/annotate";
import team from "@/store/modules/team";
import teamTask from "@/store/modules/teamTask";
import auth from "@/store/modules/auth";
import model from "@/store/modules/model"

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        labelGroup,
        dataset,
        annotate,
        team,
        teamTask,
        auth,
        model
    }
})

