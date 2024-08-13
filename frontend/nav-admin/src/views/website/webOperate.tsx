import { addDialog } from "@/components/ReDialog";
import { message } from "@/utils/message";
import creatforms, { type creatFormProps } from "./creatWebForm.vue";
import forms, { type FormProps } from "./webForm.vue";
import { updateWeb, delWeb, creatWeb } from "@/api/website";

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
    closeCallBack: async ({ options, index, args }) => {
      console.log(options, index, args);
      const { formInline } = options.props as creatFormProps;
      let text = "";
      if (args?.command === "cancel") {
        text = "您点击了取消按钮";
        message(text);
      } else if (args?.command === "sure") {
        const creatData = {
          name: formInline.name,
          order: Number(formInline.order),
          url: formInline.url,
          category_id: Number(formInline.category_id)
        };
        const createdWeb = await creatWeb(creatData);
        if (createdWeb) {
          message("Website creat successfully:");
        } else {
          message("Failed to creat Website");
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
      const text = `名称：${formInline.name} 排序：${formInline.order}`;
      if (args?.command === "cancel") {
        // 您点击了取消按钮
        message(`您点击了取消按钮，当前表单数据为 ${text}`);
      } else if (args?.command === "sure") {
        // 假设这里得到更新后的数据
        const updatedData = {
          name: formInline.name,
          icon_url: formInline.icon,
          description: formInline.description,
          order: Number(formInline.order),
          url: formInline.url,
          category_id: Number(formInline.category_id)
        };
        console.log("Updated id:", row.id);
        console.log("Updated data:", updatedData);

        const updatedWeb = await updateWeb(row.id, updatedData);

        if (updatedWeb) {
          message("Web updated successfully:");
        } else {
          message("Failed to update Web");
        }

        message(`您点击了确定按钮，当前表单数据为 ${text}`);
      }
    }
  });
}

export function handleDelete(row) {
  addDialog({
    width: "30%",
    title: "确认删除",
    contentRenderer: () => <p>是否确认删除</p>,
    closeCallBack: async ({ options, index, args }) => {
      console.log(options, index, args);
      let text = "";
      if (args?.command === "cancel") {
        text = "您点击了取消按钮";
        message(text);
      } else if (args?.command === "sure") {
        await delWeb(row.id);
        message("Web delete successfully");
      } else {
        message("Failed to delete Web");
      }
    }
  });
}
