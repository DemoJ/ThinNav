// 定义获取网址分类的函数
import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export type webResult = {
  id: number;
  name: string;
  description: string;
  icon_url: string;
  url: string;
  category_id: number;
  order: number;
  // 其他字段根据你的实际 API 返回值
};

interface webData {
  name?: string;
  description?: string;
  icon_url?: string;
  url?: string;
  category_id?: number;
  order?: number;
  // 其他你需要更新的字段
}

export const getWebs = async () => {
  try {
    const data = await http.request<webResult[]>(
      "get",
      baseUrlApi("websites/")
    );
    return data;
  } catch (error) {
    console.error("Failed to fetch websites:", error);
    return [];
  }
};

export const updateWebs = async (webId: string, updateData: webData) => {
  try {
    const url = baseUrlApi(`websites/${webId}`);
    const data = await http.request<webData>(
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
    console.error(`Failed to update website ${webId}:`, error);
    return null;
  }
};

export const delCategorie = async (webId: string) => {
  return http.request("delete", baseUrlApi(`websites/${webId}`));
};

export const creatCategory = async (creatData: webData) => {
  try {
    const url = baseUrlApi(`websites/`);
    const data = await http.request<webData>(
      "post",
      url,
      {
        headers: {
          "Content-Type": "application/json"
        }
      },
      {
        data: creatData
      }
    );
    return data;
  } catch (error) {
    console.error(`Failed to creat category:`, error);
    return null;
  }
};
