"""
PDF operation utilities for PDF Telegram Bot.
Handles PDF merging, splitting, compression, and format conversions.
"""

import io
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image
import PyPDF2
import pikepdf
from pdf2image import convert_from_path

import config


class PDFOperations:
    """Handles all PDF manipulation operations."""
    
    @staticmethod
    def merge_pdfs(pdf_paths: List[Path], output_path: Path) -> bool:
        """
        Merge multiple PDF files into a single PDF.
        
        Args:
            pdf_paths: List of paths to PDF files to merge
            output_path: Path where merged PDF should be saved
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            ValueError: If fewer than 2 PDFs provided
            Exception: If merge operation fails
        """
        if len(pdf_paths) < 2:
            raise ValueError("At least 2 PDF files are required for merging")
        
        if len(pdf_paths) > config.MAX_MERGE_FILES:
            raise ValueError(f"Maximum {config.MAX_MERGE_FILES} files can be merged at once")
        
        try:
            merger = PyPDF2.PdfMerger()
            
            # Add each PDF to merger
            for pdf_path in pdf_paths:
                if not pdf_path.exists():
                    raise FileNotFoundError(f"PDF file not found: {pdf_path}")
                merger.append(str(pdf_path))
            
            # Write merged PDF
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            
            merger.close()
            return True
        
        except Exception as e:
            print(f"Error merging PDFs: {e}")
            raise
    
    @staticmethod
    def split_pdf(
        pdf_path: Path,
        pages: str,
        output_path: Path
    ) -> Tuple[bool, int]:
        """
        Extract specific pages from a PDF file.
        
        Args:
            pdf_path: Path to source PDF
            pages: Page specification (e.g., "1-3", "1,3,5", "2-end")
            output_path: Path where extracted PDF should be saved
            
        Returns:
            Tuple[bool, int]: (Success status, number of pages extracted)
            
        Raises:
            ValueError: If page specification is invalid
            Exception: If split operation fails
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # Read source PDF
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                total_pages = len(reader.pages)
                
                # Parse page specification
                page_numbers = PDFOperations._parse_page_spec(pages, total_pages)
                
                if not page_numbers:
                    raise ValueError("No valid pages specified")
                
                # Create new PDF with specified pages
                writer = PyPDF2.PdfWriter()
                
                for page_num in page_numbers:
                    if 1 <= page_num <= total_pages:
                        writer.add_page(reader.pages[page_num - 1])  # Convert to 0-indexed
                    else:
                        raise ValueError(f"Page {page_num} is out of range (1-{total_pages})")
                
                # Write extracted pages
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                return True, len(page_numbers)
        
        except Exception as e:
            print(f"Error splitting PDF: {e}")
            raise
    
    @staticmethod
    def _parse_page_spec(spec: str, total_pages: int) -> List[int]:
        """
        Parse page specification string into list of page numbers.
        
        Args:
            spec: Page specification (e.g., "1-3", "1,3,5", "2-end")
            total_pages: Total number of pages in PDF
            
        Returns:
            List[int]: List of page numbers to extract
        """
        pages = []
        parts = spec.split(',')
        
        for part in parts:
            part = part.strip()
            
            if '-' in part:
                # Range specification (e.g., "1-3" or "2-end")
                range_parts = part.split('-')
                if len(range_parts) != 2:
                    continue
                
                start = range_parts[0].strip()
                end = range_parts[1].strip()
                
                # Handle "end" keyword
                if end.lower() == 'end':
                    end = str(total_pages)
                
                try:
                    start_num = int(start)
                    end_num = int(end)
                    pages.extend(range(start_num, end_num + 1))
                except ValueError:
                    continue
            else:
                # Single page number
                try:
                    pages.append(int(part))
                except ValueError:
                    continue
        
        # Remove duplicates and sort
        return sorted(list(set(pages)))
    
    @staticmethod
    def compress_pdf(
        pdf_path: Path,
        output_path: Path,
        quality: str = "default"
    ) -> Tuple[bool, float, float]:
        """
        Compress a PDF file to reduce its size using Ghostscript.
        
        Args:
            pdf_path: Path to source PDF
            output_path: Path where compressed PDF should be saved
            quality: Compression quality level ("low", "default", or "high")
            
        Returns:
            Tuple[bool, float, float]: (Success, original size MB, compressed size MB)
            
        Raises:
            ValueError: If quality level is invalid
            Exception: If compression fails
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if quality not in config.COMPRESSION_LEVELS:
            raise ValueError(f"Invalid quality level. Use: {', '.join(config.COMPRESSION_LEVELS.keys())}")
        
        try:
            # Get original file size
            original_size = pdf_path.stat().st_size / (1024 * 1024)
            
            # Get quality setting from config
            gs_quality = config.COMPRESSION_LEVELS[quality]
            
            # Try Ghostscript compression first (most effective)
            try:
                gs_command = [
                    'gs',
                    '-sDEVICE=pdfwrite',
                    '-dCompatibilityLevel=1.4',
                    f'-dPDFSETTINGS={gs_quality}',
                    '-dNOPAUSE',
                    '-dQUIET',
                    '-dBATCH',
                    f'-sOutputFile={output_path}',
                    str(pdf_path)
                ]
                
                result = subprocess.run(
                    gs_command,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutes timeout
                )
                
                if result.returncode == 0 and output_path.exists():
                    # Ghostscript compression successful
                    compressed_size = output_path.stat().st_size / (1024 * 1024)
                    return True, original_size, compressed_size
                else:
                    # Ghostscript failed, fall back to pikepdf
                    raise Exception("Ghostscript compression failed")
                    
            except (FileNotFoundError, subprocess.TimeoutExpired, Exception) as e:
                # Ghostscript not available or failed, use pikepdf as fallback
                print(f"Ghostscript compression failed: {e}, falling back to pikepdf")
                
                with pikepdf.open(pdf_path) as pdf:
                    # Remove unused objects and compress
                    pdf.remove_unreferenced_resources()
                    
                    # Save with compression settings
                    pdf.save(
                        output_path,
                        compress_streams=True,
                        stream_decode_level=pikepdf.StreamDecodeLevel.generalized,
                        object_stream_mode=pikepdf.ObjectStreamMode.generate,
                        recompress_flate=True
                    )
                
                compressed_size = output_path.stat().st_size / (1024 * 1024)
                return True, original_size, compressed_size
        
        except Exception as e:
            print(f"Error compressing PDF: {e}")
            raise
    
    @staticmethod
    def pdf_to_images(
        pdf_path: Path,
        output_dir: Path,
        format: str = "PNG"
    ) -> List[Path]:
        """
        Convert PDF pages to individual image files.
        Optimized for faster conversion on limited resources.
        
        Args:
            pdf_path: Path to source PDF
            output_dir: Directory where images should be saved
            format: Image format (PNG, JPEG, etc.)
            
        Returns:
            List[Path]: List of paths to generated image files
            
        Raises:
            Exception: If conversion fails
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Convert PDF to images with optimized settings
            # Reduced DPI from 200 to 150 for faster processing (still good quality)
            # Added thread_count for multi-threaded conversion
            images = convert_from_path(
                str(pdf_path),
                dpi=150,  # Reduced for faster processing while maintaining quality
                fmt=format.lower(),
                thread_count=2  # Use 2 threads for faster processing
            )
            
            image_paths = []
            
            # Save each page as separate image
            for i, image in enumerate(images, start=1):
                image_path = output_dir / f"page_{i:03d}.{format.lower()}"
                
                # For JPEG, use quality setting to balance size/quality
                if format.upper() == "JPEG":
                    image.save(str(image_path), format.upper(), quality=85, optimize=True)
                else:
                    image.save(str(image_path), format.upper(), optimize=True)
                
                image_paths.append(image_path)
            
            return image_paths
        
        except Exception as e:
            print(f"Error converting PDF to images: {e}")
            raise
    
    @staticmethod
    def images_to_pdf(
        image_paths: List[Path],
        output_path: Path
    ) -> bool:
        """
        Convert multiple images into a single PDF file.
        
        Args:
            image_paths: List of paths to image files
            output_path: Path where PDF should be saved
            
        Returns:
            bool: True if successful
            
        Raises:
            ValueError: If no valid images provided
            Exception: If conversion fails
        """
        if not image_paths:
            raise ValueError("No images provided for PDF conversion")
        
        if len(image_paths) > config.MAX_IMAGE_FILES:
            raise ValueError(f"Maximum {config.MAX_IMAGE_FILES} images can be converted at once")
        
        try:
            images = []
            
            # Open and convert all images
            for img_path in image_paths:
                if not img_path.exists():
                    print(f"Warning: Image not found: {img_path}")
                    continue
                
                # Open image and convert to RGB if necessary
                img = Image.open(img_path)
                
                # Convert to RGB (required for PDF)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                images.append(img)
            
            if not images:
                raise ValueError("No valid images could be loaded")
            
            # Save as PDF
            first_image = images[0]
            other_images = images[1:] if len(images) > 1 else []
            
            first_image.save(
                str(output_path),
                "PDF",
                save_all=True,
                append_images=other_images,
                resolution=100.0
            )
            
            return True
        
        except Exception as e:
            print(f"Error converting images to PDF: {e}")
            raise
    
    @staticmethod
    def get_pdf_info(pdf_path: Path) -> dict:
        """
        Get information about a PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            dict: PDF information (page count, size, etc.)
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                
                return {
                    'pages': len(reader.pages),
                    'size_mb': pdf_path.stat().st_size / (1024 * 1024),
                    'encrypted': reader.is_encrypted
                }
        
        except Exception as e:
            print(f"Error getting PDF info: {e}")
            return {
                'pages': 0,
                'size_mb': 0,
                'encrypted': False
            }


# Global PDF operations instance
pdf_ops = PDFOperations()