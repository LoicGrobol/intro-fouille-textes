DISTDIR = "_build"
latex_files = Rake::FileList["slides/slides_introfdt.tex", "syllabus/syllabus.tex"]
latexmk = "latexmk -lualatex -halt-on-error -shell-escape -file-line-error -interaction=nonstopmode -cd"

task default: %w[latex_dist]

directory DISTDIR

rule ".pdf" => ".tex" do |t|
  puts "\n" "Build #{t.source}."
  sh "#{latexmk} #{t.source}"
end

multitask latex_build: latex_files.ext('.pdf')

task :latex_dist => [DISTDIR, :latex_build] do
    latex_files.ext('.pdf').each do |f|
        cp f, "#{DISTDIR}/#{File.basename(f, File.extname(f))}.pdf", :verbose => true
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

task :clean => %w[clean_latex]

task :clobber => %w[clobber_dist %clobber_latex]

task :texliveonfly do
    latex_files.each do |f|
        sh "texliveonfly -c lualatex #{f} || true"
    end
    latex_files.ext('.pdf').each do |f|
        rm f
end

import "tests/Rakefile"
