import { message } from "@/utils/message";
import forms, { type FormProps } from "./form.vue";
import { updateCategory, delCategorie } from "@/api/category";
import { addDialog } from "@/components/ReDialog";

export function handleEdit(row) {
  addDialog({
    width: "30%",
    title: "编辑分类",

    contentRenderer: () => forms,
    props: {
      // 赋默认值
      formInline: {
        name: row.name,
        icon: row.icon_url,
        order: row.order
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
          order: Number(formInline.order)
        };
        console.log("Updated id:", row.id);
        console.log("Updated data:", updatedData);

        const updatedCategory = await updateCategory(row.id, updatedData);

        if (updatedCategory) {
          console.log("Category updated successfully:", updatedCategory);
        } else {
          console.log("Failed to update category");
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
        const delCategory = await delCategorie(row.id);

        if (delCategory) {
          message("Category delete successfully:", delCategory);
        } else {
          message("Failed to delete category");
        }
      }
    }
  });
}
