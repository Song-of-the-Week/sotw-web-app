import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import HomeView from "@/views/HomeView.vue";
import LoginRegisterModal from "@/components/LoginRegisterModal.vue";
import InviteModal from "@/components/InviteModal.vue";
import SotwCreationModal from "@/components/SotwCreationModal.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,

    children: [
      {
        path: "/auth/verify/:verificationToken",
        props: true,
        name: "verify",
        meta: {
          guest: true,
        },
      },
      {
        path: "register",
        props: true,
        name: "register",
        meta: {
          registerModal: true,
          guest: true,
        },
      },
      {
        path: "login",
        props: true,
        name: "login",
        meta: {
          loginModal: true,
          guest: true,
        },
      },
      {
        path: "sotw/invite/:shareToken",
        props: true,
        name: "invite",
        meta: {
          inviteModal: true,
          requiresAuth: true,
        },
      },
      {
        path: "link-spotify",
        props: true,
        name: "spotify",
        meta: {
          spotifyModal: true,
          requiresAuth: true,
        },
      },
    ],
  },
  {
    path: "/sotw/create",
    name: "create",
    props: true,
    meta: {
      createModal: true,
      requiresAuth: true,
    },
  },
  {
    path: "/sotw/:sotwId",
    name: "sotw",
    component: () => import("../views/SotwView.vue"),
    meta: {
      requiresAuth: true,
    },
    beforeEnter: (to, from, next) => {
      // Access the sotwId from route params
      const sotwId = to.params.sotwId;

      // Check if the sotwId exists in the user's sotw_list
      const userSotws = store.getters.getUser.sotw_list; // Adjust based on your Vuex structure
      const hasAccess = userSotws.some((sotw) => sotw.id === sotwId);

      if (hasAccess) {
        next(); // Proceed to the route
      } else {
        next({ name: "Home" }); // Redirect to Home if access is denied
      }
    },
  },
  {
    path: "/sotw/:sotwId/survey",
    name: "survey",
    component: () => import("../views/SotwView.vue"),
    meta: {
      requiresAuth: true,
      survey: true,
    },
  },
  {
    path: "/sotw/:sotwId/results",
    name: "results_list",
    component: () => import("../views/SotwView.vue"),
    meta: {
      requiresAuth: true,
      results: true,
    },
  },
  {
    path: "/sotw/:sotwId/results/:weekNum",
    name: "results",
    component: () => import("../views/SotwView.vue"),
    meta: {
      requiresAuth: true,
      results: true,
    },
  },
  {
    path: "/sotw/:sotwId/playlist/:weekNum",
    name: "playlist",
    component: () => import("../views/SotwView.vue"),
    meta: {
      requiresAuth: true,
      playlist: true,
    },
  },
  {
    path: "/sotw/:sotwId/playlist/soty",
    name: "soty",
    component: () => import("../views/SotwView.vue"),
    meta: {
      requiresAuth: true,
      playlist: true,
    },
  },
  {
    path: "/sotw/:sotwId/playlist/master",
    name: "playlist_list",
    component: () => import("../views/SotwView.vue"),
    meta: {
      requiresAuth: true,
      playlist: true,
    },
  },
  {
    path: "/sotw/:sotwId/members",
    name: "members",
    component: () => import("../views/SotwView.vue"),
    meta: {
      requiresAuth: true,
      playlist: true,
    },
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
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
    path: "/user/email/verify/:verificationToken",
    name: "email",
    component: () => import(/* webpackChunkName: "user" */ "../views/UserView.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/password-reset/:verificationToken",
    name: "password",
    component: () => import("../views/PasswordResetView.vue"),
  },
  {
    path: "/403",
    name: "403",
    component: () => import("../views/403View.vue"),
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
