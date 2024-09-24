import { message } from "@/utils/message";
import forms, { type FormProps } from "./cateForm.vue";
import { updateCategory, delCategory, creatCategory } from "@/api/category";
import { addDialog } from "@/components/ReDialog";

let fetchCategories: () => void; // 用于在外部调用

export function setFetchCategoriesMethod(method: () => void) {
  fetchCategories = method;
}

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
      const { formInline } = options.props as FormProps;
      if (args?.command === "sure") {
        const updatedData = {
          name: formInline.name,
          icon_url: formInline.icon,
          order: Number(formInline.order)
        };

        try {
          await updateCategory(row.id, updatedData);
          message("Category updated successfully");
          if (fetchCategories) fetchCategories(); // 更新表格数据
        } catch (error) {
          message(error.response?.data?.detail || "Failed to update category");
        }
      }
    }
  });
}

export function handleCreat() {
  addDialog({
    width: "30%",
    title: "新建分类",
    contentRenderer: () => forms,
    props: {
      // 赋默认值
      formInline: {
        name: "",
        icon: "",
        order: ""
      }
    },
    closeCallBack: async ({ options, args }) => {
      const { formInline } = options.props as FormProps;
      if (args?.command === "sure") {
        const creatData = {
          name: formInline.name,
          icon_url: formInline.icon,
          order: Number(formInline.order)
        };
        try {
          await creatCategory(creatData);
          message("Category created successfully");
          if (fetchCategories) fetchCategories(); // 更新表格数据
        } catch (error) {
          message(error.response?.data?.detail || "Failed to create category");
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
      let text = "";
      if (args?.command === "cancel") {
        text = "您点击了取消按钮";
        console.log(text);
      } else if (args?.command === "sure") {
        await delCategory(row.id);
        message("Category deleted successfully");
        if (fetchCategories) fetchCategories(); // 更新表格数据
      } else {
        message("Failed to delete category");
      }
    }
  });
}
