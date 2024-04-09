// 最简代码，也就是这些字段必须有
export default {
  path: "/account",
  meta: {
    title: "账号"
  },
  children: [
    {
      path: "/account/index",
      name: "Account",
      component: () => import("@/views/account/index.vue"),
      meta: {
        title: "修改密码",
        // 通过设置showParent为true，显示父级
        showParent: true
      }
    }
  ]
};

