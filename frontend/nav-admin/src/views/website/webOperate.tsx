import { addDialog } from "@/components/ReDialog";
import { message } from "@/utils/message";
import creatforms, { type creatFormProps } from "./creatWebForm.vue";
import forms, { type FormProps } from "./webForm.vue";
import { updateWeb, delWeb, creatWeb } from "@/api/website";

let fetchWebs: () => void; // 用于在外部调用

export function setFetchWebsMethod(method: () => void) {
  fetchWebs = method;
}

export function handleCreat() {
  addDialog({
    width: "30%",
    title: "新建网址",
    contentRenderer: () => creatforms,
    props: {
      // 赋默认值
      formInline: {
        name: "",
        order: "",
        url: "",
        category_id: ""
      }
    },
    closeCallBack: async ({ options, args }) => {
      console.log(options, args);
      const { formInline } = options.props as creatFormProps;
      if (args?.command === "sure") {
        const creatData = {
          name: formInline.name,
          order: Number(formInline.order),
          url: formInline.url,
          category_id: Number(formInline.category_id)
        };
        const createdWeb = await creatWeb(creatData);
        if (createdWeb) {
          message("Website created successfully:");
          if (fetchWebs) fetchWebs(); // 更新表格数据
        } else {
          message("Failed to create Website");
        }
      }
    }
  });
}

export function handleEdit(row) {
  addDialog({
    width: "30%",
    title: "编辑网址",
    contentRenderer: () => forms,
    props: {
      // 赋默认值
      formInline: {
        name: row.name,
        icon: row.icon_url,
        description: row.description,
        order: row.order,
        url: row.url,
        category_id: row.category_id
      }
    },
    closeCallBack: async ({ options, args }) => {
      // options.props 是响应式的
      const { formInline } = options.props as FormProps;
      if (args?.command === "sure") {
        const updatedData = {
          name: formInline.name,
          icon_url: formInline.icon,
          description: formInline.description,
          order: Number(formInline.order),
          url: formInline.url,
          category_id: Number(formInline.category_id)
        };

        const updatedWeb = await updateWeb(row.id, updatedData);

        if (updatedWeb) {
          message("Web updated successfully:");
          if (fetchWebs) fetchWebs(); // 更新表格数据
        } else {
          message("Failed to update Web");
        }
      }
    }
  });
}

export function handleDelete(row) {
  addDialog({
    width: "30%",
    title: "确认删除",
    contentRenderer: () => <p>是否确认删除</p>,
    closeCallBack: async ({ options, args }) => {
      console.log(options, args);
      let text = "";
      if (args?.command === "cancel") {
        text = "您点击了取消按钮";
        console.log(text);
      } else if (args?.command === "sure") {
        await delWeb(row.id);
        message("Web deleted successfully");
        if (fetchWebs) fetchWebs(); // 更新表格数据
      } else {
        message("Failed to delete Web");
      }
    }
  });
}
