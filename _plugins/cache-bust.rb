# based on https://distresssignal.org/busting-css-cache-with-jekyll-md5-hash
# https://gist.github.com/BryanSchuetz/2ee8c115096d7dd98f294362f6a667db
module Jekyll
  module CacheBust
    class CacheDigester
      require 'digest/md5'
      require 'pathname'

      attr_accessor :file_name, :directory

      def initialize(file_name:, directory: nil)
        self.file_name = file_name
        self.directory = directory
      end

      def digest!
        [file_name, '?', Digest::MD5.hexdigest(file_contents)].join
      end

      private

      def directory_files_content
        target_path = File.join(directory, '**', '*')
        Dir[target_path].map{|f| File.read(f) unless File.directory?(f) }.join
      end

      def file_content
        local_file_name = file_name.slice((file_name.index('assets/')..-1))
        unless File.exist?(local_file_name)
          scss_source = local_file_name.sub(/\.css\z/, '.scss')
          local_file_name = scss_source if File.exist?(scss_source)
        end
        File.read(local_file_name)
      end

      def file_contents
        is_directory? ? file_content : directory_files_content
      end

      def is_directory?
        directory.nil?
      end
    end

    def bust_file_cache(file_name)
      CacheDigester.new(file_name: file_name, directory: nil).digest!
    end

    def bust_css_cache(file_name)
      digest_parts = []
      main_scss = 'assets/css/main.scss'
      digest_parts << File.read(main_scss) if File.exist?(main_scss)

      sass_glob = File.join('assets', '_sass', '**', '*')
      Dir[sass_glob].sort.each do |path|
        digest_parts << File.read(path) unless File.directory?(path)
      end

      [file_name, '?', Digest::MD5.hexdigest(digest_parts.join)].join
    end
  end
end

Liquid::Template.register_filter(Jekyll::CacheBust)