latex_files = Rake::FileList["slides/slides_introfdt.tex", "syllabus/syllabus.tex"]
latexmk = "latexmk -lualatex -halt-on-error -shell-escape -file-line-error -interaction=nonstopmode -cd"

task default: %w[latex_build]

rule ".pdf" => ".tex" do |t|
  puts "\n" "Build #{t.source}."
  sh "#{latexmk} #{t.source}"
end

multitask latex_build: latex_files.ext('.pdf')

task :test => %w[tests:default]

task :clean_latex do
    latex_files.each do |f|
        Dir.chdir(File.dirname(f)) do
            sh "latexmk -C"
            rm_rf "tikzpics"
        end
    end
end

task :clean_dist do
    rm_rf DISTDIR
end

task :clean => %w[clean_latex clean_dist]

import "tests/Rakefile"
