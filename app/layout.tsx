import { Inter } from "next/font/google";
import "./globals.css";
import Warnings from "./components/warnings";
import { assistantId } from "./assistant-config";
const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "CS 61A Bot",
  description: "A robot tutor for CS 61A using the Assistants API with OpenAI",
  icons: {
    icon: "/robot-tutor.png",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {assistantId ? children : <Warnings />}
        <img className="logo" src="/robot-tutor.png" alt="Robot Tutor Mascot" />
      </body>
    </html>
  );
}
