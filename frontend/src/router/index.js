import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import HomeView from "@/views/HomeView.vue";
import LoginRegisterModal from "@/components/LoginRegisterModal.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,

    children: [
      {
        path: "register",
        props: true,
        component: LoginRegisterModal,
        meta: {
          registerModal: true,
          guest: true,
        },
      },
      {
        path: "login",
        props: true,
        component: LoginRegisterModal,
        meta: {
          loginModal: true,
          guest: true,
        },
      },
    ],
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/user",
    name: "user",
    component: () => import(/* webpackChunkName: "user" */ "../views/UserView.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "404",
    component: () => import("../views/404View.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Handle routes with `requiresAuth` meta key
    if (store.getters.isAuthenticated) {
      next();
      return;
    }
    sessionStorage.setItem("last_requested_path", to.path);
    next("/login");
  } else if (to.matched.some((record) => record.meta.guest)) {
    // Handle routes with `guest` meta key
    if (store.getters.isAuthenticated) {
      next("/");
      return;
    }
    next();
  } else {
    next();
  }
});

export default router;
