FROM heartexlabs/label-studio:latest

# Create necessary directories
RUN mkdir -p /label-studio/data /label-studio/files

# Set environment variables
ENV LABEL_STUDIO_DATABASE=sqlite:///label-studio/data/label_studio.sqlite3
ENV LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
ENV LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/label-studio/files

# Set user
USER 1001

# Expose port
EXPOSE 8080

# Set working directory
WORKDIR /label-studio

# Command to run the application
CMD ["label-studio"] 