import VueRouter from "vue-router";
import LabelGroupView from "@/views/LabelGroupView";
import DatasetView from "@/views/DatasetView";
import AnnotateView from "@/views/AnnotateView";
import LoginOrSignupView from "@/views/LoginOrSignupView";
import TeamTaskView from "@/views/TeamTaskView";
import TeamView from "@/views/TeamView";
import TheContent from "@/layouts/TheContent";
import AIModelView from "@/views/AIModelView";
import DatasetImageView from "@/views/DatasetImageView";
import DetectView from "@/views/DetectView";
import AIModelDetail from "@/components/AIModelDetail";

const router = new VueRouter({
    routes:[
        {
            path: '/login',
            name: 'login',
            component: LoginOrSignupView
        },
        {
            path: '/signup',
            name: 'signup',
            component: LoginOrSignupView
        },
        {
            path: '/',
            component: TheContent,
            redirect: '/dataset',
            children:[
                {
                    path: '/dataset',
                    name: 'dataset',
                    component: DatasetView
                },
                {
                    path: '/dataset/:id',
                    component: DatasetImageView
                },
                {
                    path: '/label-groups',
                    name: 'label-group',
                    component: LabelGroupView,
                },
                {
                    path: '/annotate',
                    component: AnnotateView
                },
                {
                    path: '/task',
                    component: TeamTaskView
                },
                {
                    path: '/team',
                    component: TeamView
                },
                {
                    path: '/model',
                    component: AIModelView
                },
                {
                    path:  '/model/:id',
                    component: AIModelDetail
                },
                {
                    path: '/detect',
                    component: DetectView
                }
            ]
        },

    ]
})

export default router