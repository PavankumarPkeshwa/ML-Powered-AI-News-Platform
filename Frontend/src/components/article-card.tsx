import { Link } from "wouter";
import { Heart } from "lucide-react";
import type { Article } from "@shared/schema";

interface ArticleCardProps {
  article: Article;
  variant?: "default" | "compact";
}

export default function ArticleCard({ article, variant = "default" }: ArticleCardProps) {
  const getCategoryColor = (category: string) => {
    const colorMap: Record<string, string> = {
      Technology: "bg-tech",
      Lifestyle: "bg-lifestyle",
      Sports: "bg-sports",
      Fitness: "bg-fitness",
      Food: "bg-food",
      Travel: "bg-travel",
    };
    return colorMap[category] || "bg-gray-500";
  };

  const formatDate = (date: Date | string) => {
    return new Date(date).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  if (variant === "compact") {
    return (
      <Link href={`/article/${article.id}`}>
        <div className="flex space-x-4 p-4 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors cursor-pointer">
          <img
            src={article.imageUrl}
            alt={article.title}
            className="w-20 h-16 object-cover rounded-lg flex-shrink-0"
          />
          <div className="flex-1 min-w-0">
            <span className={`inline-block px-2 py-1 text-white text-xs font-medium rounded mb-2 ${getCategoryColor(article.category)}`}>
              {article.category}
            </span>
            <h4 className="font-semibold text-sm mb-1 line-clamp-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors dark:text-white">
              {article.title}
            </h4>
            <p className="text-xs text-gray-600 dark:text-gray-400">
              {formatDate(article.publishDate)}
            </p>
          </div>
        </div>
      </Link>
    );
  }

  return (
    <Link href={`/article/${article.id}`}>
      <article className="bg-white dark:bg-gray-800 rounded-xl shadow-sm hover:shadow-md dark:hover:shadow-blue-500/10 transition-shadow duration-300 overflow-hidden group cursor-pointer border border-transparent dark:border-gray-700">
        <img
          src={article.imageUrl}
          alt={article.title}
          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <div className="p-6">
          <div className="flex items-center justify-between mb-3">
            <span className={`inline-block px-3 py-1 text-white text-xs font-medium rounded-full ${getCategoryColor(article.category)}`}>
              {article.category}
            </span>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {formatDate(article.publishDate)}
            </span>
          </div>
          <h3 className="text-lg font-semibold mb-2 line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors dark:text-white">
            {article.title}
          </h3>
          <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-3">
            {article.excerpt}
          </p>
          <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
            <div className="flex items-center space-x-2">
              <span>{article.author}</span>
              <span>•</span>
              <span>{article.readTime}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Heart className="h-4 w-4 text-gray-400 dark:text-gray-500" />
              <span>{article.likes}</span>
            </div>
          </div>
        </div>
      </article>
    </Link>
  );
}
