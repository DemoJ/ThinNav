// 最简代码，也就是这些字段必须有
export default {
  path: "/website",
  meta: {
    title: "网站管理"
  },
  children: [
    {
      path: "/website/category",
      name: "Category",
      component: () => import("@/views/website/category.vue"),
      meta: {
        title: "网站分类"
      }
    },
    {
      path: "/website/website",
      name: "Website",
      component: () => import("@/views/website/website.vue"),
      meta: {
        title: "网站列表"
      }
    }
  ]
};


