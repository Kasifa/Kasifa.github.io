import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Navier–Stokes 开放研究日志",
  description:
    "三维不可压缩 Navier–Stokes 存在性与光滑性问题：研究综述、攻关计划与公开研究日志。",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
