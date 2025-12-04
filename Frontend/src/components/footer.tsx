import { Link } from "wouter";
import { categories } from "@shared/schema";

export default function Footer() {
  return (
    <footer className="bg-white dark:bg-gray-900 border-t dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="md:col-span-1">
            <Link href="/">
              <div className="flex items-center space-x-2 mb-4 cursor-pointer group">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">P</span>
                </div>
                <h3 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Pavan-Insight-Global
                </h3>
              </div>
            </Link>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
              Your trusted source for the latest news and insights across technology, lifestyle, sports, fitness, food, and travel. Delivering quality journalism and expert analysis.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                <i className="fab fa-twitter text-lg"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-600 transition-colors">
                <i className="fab fa-facebook text-lg"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-600 transition-colors">
                <i className="fab fa-instagram text-lg"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-600 transition-colors">
                <i className="fab fa-linkedin text-lg"></i>
              </a>
            </div>
          </div>

          {/* Categories */}
          <div>
            <h4 className="font-semibold mb-4 dark:text-white">Categories</h4>
            <ul className="space-y-2 text-sm">
              {categories.map((category) => (
                <li key={category}>
                  <Link href={`/category/${category.toLowerCase()}`} className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                    {category}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="font-semibold mb-4 dark:text-white">Company</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">About Us</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Our Team</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Careers</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Contact</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Advertise</a></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-semibold mb-4 dark:text-white">Legal</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Terms of Service</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Cookie Policy</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">GDPR</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t dark:border-gray-800 pt-8 mt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-600 dark:text-gray-400 text-sm">© 2024 Pavan-Insight-Global. All rights reserved.</p>
            <div className="flex items-center space-x-6 mt-4 md:mt-0">
              <span className="text-xs text-gray-500 dark:text-gray-400">Made with ❤️ for readers worldwide</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
