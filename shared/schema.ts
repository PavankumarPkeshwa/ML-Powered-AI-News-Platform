export const categories = ["Technology", "Business", "Science", "Health", "Sports", "Entertainment"] as const;
export type Category = typeof categories[number];

export type InsertArticle = {
  title: string;
  excerpt: string;
  content: string;
  category: Category;
  author: string;
  imageUrl: string;
  publishDate: Date;
  readTime: string;
  likes?: number;
  isFeatured?: boolean;
  isTrending?: boolean;
};
export type Article = InsertArticle & {
  id: string; 
};