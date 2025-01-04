import "@/styles/globals.css";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

interface IRootLayoutProps {
	children: React.ReactNode;
}

export default function RootLayout(props: IRootLayoutProps) {
	const { children } = props;
	
	return (
		<html lang="en">
			<head></head>
			<body>
				{children}
				<ToastContainer
					hideProgressBar={true}
					autoClose={2000}
				/>
				<div id="modal" />
			</body>
		</html>
	)
}