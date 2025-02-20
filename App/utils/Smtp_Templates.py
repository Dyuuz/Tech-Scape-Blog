def send_verification_email(username, verify_account_link, cs_url):
    html_message = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <title>Verify Your Account</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f3f6fb;
                color: #333;
            }}
            .email-container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                overflow: hidden;
                border: 1px solid #dcdcdc;
            }}
            .email-header {{
                background: linear-gradient(135deg,rgb(27, 52, 76), #3498db);
                color: #ffffff;
                padding: 30px 20px;
                text-align: center;
            }}
            .email-header h1 {{
                margin: 0;
                font-size: 28px;
                letter-spacing: 1px;
            }}
            .email-body {{
                padding: 30px 20px;
                padding-bottom:0px;
                text-align: center;
            }}
            .email-body p {{
                font-size: 18px;
                margin: 15px 0;
                line-height: 1.6;
            }}
            .verify-button {{
                display: inline-block;
                padding: 14px 24px;
                margin: 30px 0;
                background: linear-gradient(135deg,rgb(27, 52, 76), #3498db);
                color: #ffffff;
                text-decoration: none;
                border-radius: 6px;
                font-size: 18px;
                transition: background-color 0.3s ease;
            }}
            .verify-button:hover {{
                background-color: #2980b9;
            }}
            .email-footer1 {{
                padding: 20px;
                text-align: center;
                font-size: 14px;
                color: #777;
            }}
            .email-footer a {{
                color: #3498db;
                text-decoration: none;
            }}
            @media (max-width: 480px) {{
                .email-header h1 {{
                    font-size: 24px;
                }}
                .email-body p {{
                    font-size: 16px;
                }}
                .verify-button {{
                    padding: 12px 20px;
                    font-size: 16px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>Verify Your Account</h1>
            </div>
            <div class="email-body">
                <p>Hello <strong>{username}</strong>,</p>
                <p>Thank you for signing up with <strong>TechScape</strong>.</p>
                <p>Please click the button below to verify your email address and activate your account.</p>
                <p>NB: You will be unable to use our service if you fail to verify.</p>
                <p>Verification is instant, just one click away.</p>
                <a href="{verify_account_link}" class="verify-button">🔐 Verify My Account</a>
                <p>If you did not create this account, please ignore this message.</p>
            </div>
            <div class="email-footer1">
                <p>Need help? <a href="{cs_url}">Visit our support center</a></p>
                <p>&copy; 2025 TechScape. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_message

def verified_user_feedback(username, url, cs_url):
    html_message = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <title>Verify Your Account</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f3f6fb;
                color: #333;
            }}
            .email-container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                overflow: hidden;
                border: 1px solid #dcdcdc;
            }}
            .email-header {{
                background: linear-gradient(135deg,rgb(60, 94, 127), #3498db);
                color: #ffffff;
                padding: 30px 20px;
                text-align: center;
            }}
            .email-header h1 {{
                margin: 0;
                font-size: 28px;
                letter-spacing: 1px;
            }}
            .email-body {{
                padding: 30px 20px;
                padding-bottom:0px;
                text-align: center;
            }}
            .email-body a{{
                background: linear-gradient(135deg, #2c3e50, #3498db);
            }}
            .email-body h5{{
                text-align:left;
                margin-left: 10px;
            }}
            .email-body p {{
                font-size: 18px;
                margin: 15px 0;
                line-height: 1.6;
            }}
            .verify-button {{
                display: inline-block;
                padding: 14px 24px;
                margin: 30px 0;
                background-color: #3498db;
                color: #ffffff;
                text-decoration: none;
                border-radius: 6px;
                font-size: 18px;
                transition: background-color 0.3s ease;
            }}
            .verify-button:hover {{
                background-color: #2980b9;
            }}
            .email-footer {{
                padding: 20px;
                text-align: center;
                font-size: 14px;
                color: #777;
            }}
            .email-footer a {{
                color: #3498db;
                text-decoration: none;
            }}
            @media (max-width: 480px) {{
                .email-header h1 {{
                    font-size: 24px;
                }}
                .email-body p {{
                    font-size: 16px;
                }}
                .verify-button {{
                    padding: 12px 20px;
                    font-size: 16px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>Account Verified!</h1>
            </div>
            <div class="email-body">
                <p>Hello <strong>{username}</strong>,</p>
                <p>Welcome to <strong>TechScape.</strong> We’re excited to have you here.</p>
                <p>You’ve just joined a community of curious minds and deep thinkers!<br>
                    Your account is now verified, which means you’re all set to dive into inspiring articles and explore fresh perspectives.<br><br>
                    ✨ What’s Next?<br>
                    ✔️Explore Our Blog – Discover insightful articles and valuable resources.<br>
                    ✔️Engage with Content – Like and share posts that resonate with you. Your feedback helps shape future topics!<br>
                    ✔️Stay Updated – Subscribe to our newsletter and never miss an update from us.<br>
                    ✔️Follow Us on Social Media – Get exclusive content, behind-the-scenes insights, and real-time updates.<br>
                    ✔️Suggest Topics – Have something you’d love to read about? Reply to this email or use our suggestion box!<br>
                    ✔️Subscribe to our newsletter for exclusive content!
                </p>
                <a href="{url}" class="verify-button">Start Exploring</a>
                <p>
                    🚀 Exciting Updates Coming Soon!<br>
                    We’re working on exclusive content drops, special features, and surprise announcements that you won’t want to miss! Stay tuned for something amazing! Happy reading! 📚✨
                </p>
                <h5>
                    Cheers,<br>
                    The TechScape Team.<br>
                </h5>
            </div>
            <div class="email-footer">
                <p>Need help? <a href="{cs_url}">Visit our support center</a></p>
                <p>&copy; 2025 TechScape. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_message

def send_password_reset_email(username, reset_link, cs_url):
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
           body {{ background-color: #fff5f7; color: #333; font-family: 'Helvetica', sans-serif; text-align: center; }}
            .email-container {{ max-width: 600px; margin: 30px auto; background: #fff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); padding: 30px; }}
            .email-header {{ font-size: 24px; margin-bottom: 20px; color: #e74c3c; }}
            .reset-button {{ display: inline-block; margin: 20px 0; background: linear-gradient(170deg, #081b3e, #6a8caf); color: #fff; padding: 14px 24px; border-radius: 6px; text-decoration: none; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <p>Hello <strong>{username}</strong>,</p>
            <p>We received a request to reset your password. Link will expire in 15 minutes.</p>
            <p>Click the button below to proceed:</p>
            <a class="reset-button" href="{reset_link}">Reset Password</a>
            <p>If you didn't request this, please ignore this email.</p>
            <p>Need help? <a href="{cs_url}">Visit our support center</a></p>
            <div class="footer">© 2025 TechScape. All rights reserved.</div>
        </div>
    </body>
    </html>
    """
    return html_message

def send_password_reset_success_mail(username, password, cs_url):
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
           body {{ background-color: #fff5f7; color: #333; font-family: 'Helvetica', sans-serif; text-align: center; }}
            .email-container {{ max-width: 600px; margin: 30px auto; background: #fff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); padding: 30px; }}
            .email-header {{ font-size: 24px; margin-bottom: 20px; color: #e74c3c; }}
            .reset-button {{ display: inline-block; margin: 20px 0; background: linear-gradient(170deg, #081b3e, #6a8caf); color: #fff; padding: 14px 24px; border-radius: 6px; text-decoration: none; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <p>Hello <strong>{username}</strong>,</p>
            <p>Your password has been successfully reset. You can now log in with your new credentials.</p>
            <p>Here's your new password:</p>
            <a class="reset-button">{password}</a>
            <p>If you didn't request this change, please contact support immediately.</p>
            <p>Need help? <a href="{cs_url}">Visit our support center</a></p>
            <div class="footer">© 2025 TechScape. All rights reserved.</div>
        </div>
    </body>
    </html>
    """
    return html_message

def send_login_email(username, reset_link):
    html_message = f"""
    <html>
    <head>
        <style>
           body {{ background-color: #fff5f7; color: #333; font-family: 'Helvetica', sans-serif; text-align: center; }}
            .email-container {{ max-width: 600px; margin: 30px auto; background: #fff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); padding: 30px; }}
            .email-header {{ font-size: 24px; margin-bottom: 20px; color: #e74c3c; }}
            .reset-button {{ display: inline-block; margin: 20px 0; background: linear-gradient(170deg, #081b3e, #6a8caf); color: #fff; padding: 14px 24px; border-radius: 6px; text-decoration: none; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <p>Hello <strong>{username}</strong>,</p>
            <p>We received a request to reset your password. Link will expire in 15 minutes.</p>
            <p>Click the button below to proceed:</p>
            <a class="reset-button" href="{reset_link}">Reset Password</a>
            <p>If you didn't request this, please ignore this email.</p>
            <div class="footer">© 2025 TechScape</div>
        </div>
    </body>
    </html>
    """
    return html_message

def send_subcribe_email(username, reset_link):
    html_message = f"""
    <html>
    <head>
        <style>
           body {{ background-color: #fff5f7; color: #333; font-family: 'Helvetica', sans-serif; text-align: center; }}
            .email-container {{ max-width: 600px; margin: 30px auto; background: #fff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); padding: 30px; }}
            .email-header {{ font-size: 24px; margin-bottom: 20px; color: #e74c3c; }}
            .reset-button {{ display: inline-block; margin: 20px 0; background: linear-gradient(170deg, #081b3e, #6a8caf); color: #fff; padding: 14px 24px; border-radius: 6px; text-decoration: none; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <p>Hello <strong>{username}</strong>,</p>
            <p>We received a request to reset your password. Link will expire in 15 minutes.</p>
            <p>Click the button below to proceed:</p>
            <a class="reset-button" href="{reset_link}">Reset Password</a>
            <p>If you didn't request this, please ignore this email.</p>
            <div class="footer">© 2025 TechScape</div>
        </div>
    </body>
    </html>
    """
    return html_message

def send_unsubscribe_email(username, reset_link):
    html_message = f"""
    <html>
    <head>
        <style>
           body {{ background-color: #fff5f7; color: #333; font-family: 'Helvetica', sans-serif; text-align: center; }}
            .email-container {{ max-width: 600px; margin: 30px auto; background: #fff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); padding: 30px; }}
            .email-header {{ font-size: 24px; margin-bottom: 20px; color: #e74c3c; }}
            .reset-button {{ display: inline-block; margin: 20px 0; background: linear-gradient(170deg, #081b3e, #6a8caf); color: #fff; padding: 14px 24px; border-radius: 6px; text-decoration: none; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <p>Hello <strong>{username}</strong>,</p>
            <p>We received a request to reset your password. Link will expire in 15 minutes.</p>
            <p>Click the button below to proceed:</p>
            <a class="reset-button" href="{reset_link}">Reset Password</a>
            <p>If you didn't request this, please ignore this email.</p>
            <div class="footer">© 2025 TechScape</div>
        </div>
    </body>
    </html>
    """
    return html_message

def newsletter_mail( username):
    html_message = f"""
    <html>
    <head>
        <style>
            body {{ background-color: #121212; color: #e0e0e0; font-family: 'Helvetica Neue', sans-serif; margin: 0; padding: 0; }}
            .email-container {{ max-width: 700px; margin: 40px auto; background: #1e1e1e; border-radius: 20px; box-shadow: 0 6px 12px rgba(0,0,0,0.5); padding: 40px; }}
            .header {{ font-size: 32px; color: #00ffc4; margin-bottom: 25px; text-align: center; }}
            .article {{ margin: 30px 0; padding: 20px; border-left: 5px solid #00ffc4; background: #2b2b2b; border-radius: 12px; }}
            .article h3 {{ color: #ff9800; margin-bottom: 10px; }}
            .article p {{ font-size: 15px; line-height: 1.6; }}
            .cta-button {{ display: inline-block; margin-top: 20px; padding: 15px 30px; background: #00ffc4; color: #000; text-decoration: none; border-radius: 10px; font-weight: 600; }}
            .footer {{ margin-top: 35px; text-align: center; font-size: 13px; color: #aaa; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">⚡ TechWave Weekly - Hello {username}!</div>
            <p>Here's what happened in the world of tech this week:</p>

            <div class="article">
                <h3>🚀 Quantum Computing Breakthrough</h3>
                <p>Researchers achieved a new milestone in quantum computing that could redefine computing power forever.</p>
            </div>

            <div class="article">
                <h3>📱 The Rise of AI-Powered Smartphones</h3>
                <p>Tech giants are integrating AI models into their latest devices, enhancing user experience dramatically.</p>
            </div>

            <a class="cta-button" href="https://techwave.com/latest">Read More</a>
            <div class="footer">© 2024 TechWave Weekly | <a href="#" style="color:#aaa;">Unsubscribe</a></div>
        </div>
    </body>
    </html>
    """
    return html_message