require 'tmpdir'

DISTDIR = "_build"
pdf_files = Rake::FileList["slides/slides_introfdt.pdf", "syllabus/syllabus.pdf"]
latexmk = "latexmk -lualatex -halt-on-error -shell-escape -file-line-error -interaction=nonstopmode -cd"

task default: %w[latex_dist]

directory DISTDIR
directory

rule ".pdf" => ".tex" do |t|
  puts "\n" "Build #{t.source}."
  sh "#{latexmk} #{t.source}"
end

multitask latex_build: pdf_files

task :latex_dist => [DISTDIR, :latex_build] do
    pdf_files.each do |f|
        cp f, "#{DISTDIR}/#{File.basename(f)}", :verbose => true
    end
end

task :test => %w[tests:default]

task :clean_latex do
    latex_files.each do |f|
        Dir.chdir(File.dirname(f)) do
            sh "latexmk -c"
            rm_rf "tikzpics"
        end
    end
end

task :clobber_latex do
    latex_files.each do |f|
        Dir.chdir(File.dirname(f)) do
            sh "latexmk -C"
            rm_rf "tikzpics"
        end
    end
end

task :clobber_dist do
    rm_rf DISTDIR
end

task :clean => %w[clean_latex tests:clean]

task :clobber => %w[clean clobber_dist %clobber_latex]

task :texliveonfly do
    latex_files.each do |f|
        sh "texliveonfly -c lualatex #{f} -a '-outdir=#{Dir.tempdir()}' || true"
    end
end

import "tests/Rakefile"
