"""
Generate and populate JWT secrets for ChatProxy Platform services.
Automatically updates .env files with secure, matching JWT secrets.

Author: Enoch Sit
License: MIT
"""

import os
import secrets
import string
import re
from pathlib import Path
from typing import Dict, List, Tuple


class SecretGenerator:
    """Generate cryptographically secure secrets for JWT and database passwords."""
    
    @staticmethod
    def generate_jwt_secret(length: int = 64) -> str:
        """
        Generate a secure JWT secret using cryptographically strong random.
        
        Args:
            length: Length of the secret (default 64 characters)
            
        Returns:
            Secure random string suitable for JWT signing
        """
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def generate_password(length: int = 32) -> str:
        """
        Generate a secure database password.
        
        Args:
            length: Length of the password (default 32 characters)
            
        Returns:
            Secure random password
        """
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_=+"
        return ''.join(secrets.choice(alphabet) for _ in range(length))


class EnvFileUpdater:
    """Update .env files with generated secrets."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.services = [
            "auth-service",
            "accounting-service",
            "flowise-proxy-service-py"
        ]
        
    def read_env_file(self, service: str) -> Tuple[List[str], Dict[str, str]]:
        """
        Read .env file and parse existing variables.
        
        Args:
            service: Service name (e.g., 'auth-service')
            
        Returns:
            Tuple of (lines, variables_dict)
        """
        env_path = self.workspace_root / service / ".env"
        
        if not env_path.exists():
            raise FileNotFoundError(f".env file not found: {env_path}")
        
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        variables = {}
        for line in lines:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                variables[key.strip()] = value.strip()
        
        return lines, variables
    
    def write_env_file(self, service: str, lines: List[str]):
        """
        Write updated lines to .env file with backup.
        
        Args:
            service: Service name
            lines: Updated lines to write
        """
        env_path = self.workspace_root / service / ".env"
        backup_path = self.workspace_root / service / ".env.backup"
        
        # Create backup
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
        
        # Write updated content
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    def update_jwt_secrets(self, access_secret: str, refresh_secret: str) -> Dict[str, bool]:
        """
        Update JWT secrets in all three services with the same values.
        
        Args:
            access_secret: JWT access token secret
            refresh_secret: JWT refresh token secret
            
        Returns:
            Dict mapping service names to success status
        """
        results = {}
        
        for service in self.services:
            try:
                lines, variables = self.read_env_file(service)
                
                # Update lines
                updated_lines = []
                access_updated = False
                refresh_updated = False
                
                for line in lines:
                    stripped = line.strip()
                    
                    # Update JWT_ACCESS_SECRET
                    if stripped.startswith('JWT_ACCESS_SECRET='):
                        updated_lines.append(f'JWT_ACCESS_SECRET={access_secret}\n')
                        access_updated = True
                    # Update JWT_REFRESH_SECRET
                    elif stripped.startswith('JWT_REFRESH_SECRET='):
                        updated_lines.append(f'JWT_REFRESH_SECRET={refresh_secret}\n')
                        refresh_updated = True
                    else:
                        updated_lines.append(line)
                
                # Append if not found
                if not access_updated:
                    updated_lines.append(f'\n# Generated JWT Secrets\nJWT_ACCESS_SECRET={access_secret}\n')
                if not refresh_updated:
                    updated_lines.append(f'JWT_REFRESH_SECRET={refresh_secret}\n')
                
                # Write back
                self.write_env_file(service, updated_lines)
                results[service] = True
                
            except Exception as e:
                print(f"❌ Error updating {service}: {e}")
                results[service] = False
        
        return results


class ColorPrinter:
    """Print colored console output for Windows."""
    
    # ANSI color codes (work in Windows Terminal and modern cmd)
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    @classmethod
    def print_header(cls, text: str):
        """Print a colored header."""
        print(f"\n{cls.BOLD}{cls.CYAN}{'═' * 70}{cls.RESET}")
        print(f"{cls.BOLD}{cls.CYAN}{text}{cls.RESET}")
        print(f"{cls.BOLD}{cls.CYAN}{'═' * 70}{cls.RESET}\n")
    
    @classmethod
    def print_success(cls, text: str):
        """Print success message."""
        print(f"{cls.GREEN}✓ {text}{cls.RESET}")
    
    @classmethod
    def print_warning(cls, text: str):
        """Print warning message."""
        print(f"{cls.YELLOW}⚠ {text}{cls.RESET}")
    
    @classmethod
    def print_error(cls, text: str):
        """Print error message."""
        print(f"{cls.RED}✗ {text}{cls.RESET}")
    
    @classmethod
    def print_info(cls, text: str):
        """Print info message."""
        print(f"{cls.BLUE}ℹ {text}{cls.RESET}")


def main():
    """Main execution function."""
    printer = ColorPrinter()
    
    # Print header
    printer.print_header("ChatProxy Platform - JWT Secret Generator")
    
    # Get workspace root
    workspace_root = Path(__file__).parent
    printer.print_info(f"Workspace: {workspace_root}")
    
    # Check if .env files exist
    printer.print_info("Checking for .env files...")
    services = ["auth-service", "accounting-service", "flowise-proxy-service-py"]
    missing_files = []
    
    for service in services:
        env_path = workspace_root / service / ".env"
        if env_path.exists():
            printer.print_success(f"{service}/.env found")
        else:
            printer.print_error(f"{service}/.env NOT FOUND")
            missing_files.append(service)
    
    if missing_files:
        print()
        printer.print_error("Missing .env files! Run setup_env_files.bat first.")
        printer.print_info("Command: setup_env_files.bat")
        return 1
    
    # Generate secrets
    print()
    printer.print_info("Generating cryptographically secure JWT secrets...")
    
    generator = SecretGenerator()
    jwt_access_secret = generator.generate_jwt_secret(64)
    jwt_refresh_secret = generator.generate_jwt_secret(64)
    
    printer.print_success(f"JWT_ACCESS_SECRET: {jwt_access_secret[:20]}... (64 chars)")
    printer.print_success(f"JWT_REFRESH_SECRET: {jwt_refresh_secret[:20]}... (64 chars)")
    
    # Update .env files
    print()
    printer.print_info("Updating .env files with JWT secrets...")
    
    updater = EnvFileUpdater(workspace_root)
    results = updater.update_jwt_secrets(jwt_access_secret, jwt_refresh_secret)
    
    # Print results
    print()
    success_count = sum(1 for success in results.values() if success)
    
    for service, success in results.items():
        if success:
            printer.print_success(f"{service}/.env updated with JWT secrets")
        else:
            printer.print_error(f"{service}/.env update FAILED")
    
    # Summary
    print()
    printer.print_header("Summary")
    
    if success_count == len(services):
        printer.print_success(f"All {success_count} services updated successfully!")
        printer.print_success("Same JWT secrets copied to all three services")
        print()
        printer.print_info("Backups created: <service>/.env.backup")
        printer.print_info("Next step: Start services with docker compose")
        return 0
    else:
        printer.print_warning(f"Updated {success_count}/{len(services)} services")
        printer.print_error("Some updates failed. Check errors above.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        exit(130)
    except Exception as e:
        ColorPrinter.print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
