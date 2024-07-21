// 定义获取网址分类的函数
import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export type CategoryResult = {
  id: number;
  name: string;
  icon_url: string;
  order: number;
  // 其他字段根据你的实际 API 返回值
};

interface CategoryUpdateData {
  name?: string;
  icon_url?: string;
  order?: number;
  // 其他你需要更新的字段
}

export const getCategories = async () => {
  try {
    const data = await http.request<CategoryResult[]>(
      "get",
      baseUrlApi("categories/")
    );
    return data;
  } catch (error) {
    console.error("Failed to fetch categories:", error);
    return [];
  }
};

export const updateCategory = async (
  categoryId: string,
  updateData: CategoryUpdateData
) => {
  try {
    const url = baseUrlApi(`categories/${categoryId}`);
    const data = await http.request<CategoryUpdateData>(
      "put",
      url,
      {
        headers: {
          "Content-Type": "application/json"
        }
      },
      {
        data: updateData
      }
    );
    return data;
  } catch (error) {
    console.error(`Failed to update category ${categoryId}:`, error);
    return null;
  }
};

export const delCategorie = async (categoryId: string) => {
  try {
    const data = await http.request(
      "delete",
      baseUrlApi(`categories/${categoryId}`)
    );
    if (data.status === 204) {
      console.log("Category deleted successfully");
      return true;
    }
    return data; // 处理其他可能的响应
  } catch (error) {
    console.error("Failed to delete categories:", error);
    return null;
  }
};
